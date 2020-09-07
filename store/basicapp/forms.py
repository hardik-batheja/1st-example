from django import forms
from django.contrib.auth.models import User
from basicapp.models import UserProfileInfo,UserDealers,UserStock


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(max_length=200)
    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'name')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('picture',)

class EntryForm(forms.ModelForm):
    def __init__(self,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dealer'].queryset = UserDealers.objects.filter(owner=user)
    class Meta():
        model=UserStock
        fields = ('item', 'company', 'rate', 'mrp', 'dealer')
        widgets={
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'dealer': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'mrp': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DealerForm(forms.ModelForm):
    dealer = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta():
        model=UserDealers
        fields=('dealer','contact')
