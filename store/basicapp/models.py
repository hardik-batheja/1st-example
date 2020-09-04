from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    name = models.CharField(max_length=200,default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class UserDealers(models.Model):
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    dealer=models.CharField(max_length=200)
    contact = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.dealer

class UserStock(models.Model):
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, default=None)
    dealer = models.ForeignKey(UserDealers, on_delete=models.CASCADE)
    item=models.CharField(max_length=200)
    company = models.CharField(max_length=200, null=True, blank=True, default=None)
    rate=models.FloatField(null=True, blank=True, default=None)
    mrp = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.item
