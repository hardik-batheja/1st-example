from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView
# Create your views here.
from django.shortcuts import render
from basicapp.forms import UserForm, UserProfileInfoForm,EntryForm,DealerForm,EditForm
from django.contrib import messages
from basicapp.models import UserProfileInfo,UserDealers,UserStock,RecycleBin
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
class index(TemplateView):
    template_name='basicapp/index.html'

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!\n Now you can access your database.")


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'basicapp/register.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basicapp/login.html', {})


class viewdb(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            itemlist=UserStock.objects.filter(owner__username=request.user.username).order_by('dealer','item')
            contdict={'records': itemlist}
            return render(request, 'basicapp/view.html',contdict)
        else:
            return render(request,'basicapp/login.html')

class dbms(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            entry_form = EntryForm(request.user, request.POST)
            dealer_form = DealerForm()
            itemlist=UserStock.objects.filter(owner__username=request.user.username).order_by('dealer','item')
            return render(request, 'basicapp/dbms.html', {'entry_form': entry_form, 'dealer_form': dealer_form,'records':itemlist})
        else:
            return render(request, 'basicapp/login.html')
    def post(self,request,*args,**kwargs):
        
        itemlist = UserStock.objects.filter(
        owner__username=request.user.username).order_by('dealer', 'item')
        if 'add_d' in request.POST:
            entry_form = EntryForm(request.user)
            dealer_form = DealerForm(request.POST)
            if dealer_form.is_valid():
                dealer=dealer_form.save(commit=False)
                dealer.owner=request.user
                dealer.save()
        if 'add_e' in request.POST:
            entry_form = EntryForm(request.user, request.POST)
            dealer_form = DealerForm()
            if entry_form.is_valid():
                entry=entry_form.save(commit=False)
                entry.owner=request.user
                if entry.item:
                    entry.item = entry.item.upper()
                if entry.company:
                    entry.company = entry.company.upper()
                entry.save()
        return render(request, 'basicapp/dbms.html', {'entry_form': entry_form, 'dealer_form': dealer_form, 'records': itemlist})

def edit(request,id):
    item = UserStock.objects.get(id=id)
    if item.owner==request.user:
        dealerlist = UserDealers.objects.filter(owner__username=request.user.username)
        return render(request,'basicapp/edit.html',{'row': item,'dealers': dealerlist})
    else:
        return HttpResponse("Access Denied!")

def update(request,id):
    item = UserStock.objects.get(id=id)
    if item.owner==request.user:
        form=EditForm(request.POST,instance=item)
        if form.is_valid():
            print("YES")
            updateform=form.save(commit=False)
            updateform.dealer.dealer=request.POST.get('dealer')
            updateform.user=request.user
            if updateform.item:
                updateform.item = updateform.item.upper()
            if updateform.company:
                updateform.company = updateform.company.upper()
            updateform.save()
            return redirect("/harry/view/")
        else:
            print(form.errors)
        return render(request, 'basicapp/edit.html', {'row': item})
    else:
        return HttpResponse("Access Denied!")

def bin(request,id):
    item = UserStock.objects.get(id=id)
    if item.owner == request.user:
        binitem = RecycleBin(owner=request.user, dealer=item.dealer,item=item.item, company=item.company, rate=item.rate, mrp=item.mrp)
        binitem.save()
        item.delete()
        return redirect("/harry/view/")
    else:
        return HttpResponse("Access Denied!")

def createorder(request):
    if request.user.is_authenticated:
        return render(request, 'basicapp/order.html')
    else:
        return render(request, 'basicapp/login.html')
