from django.contrib import admin
from basicapp.models import UserProfileInfo, User,UserDealers,UserStock

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(UserDealers)
admin.site.register(UserStock)
