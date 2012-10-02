from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.ForeignKey(User)

class OhmageAccount(models.Model):
    profile = models.OneToOneField(Profile)

    server = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    hashedpass = models.CharField(max_length=200,null=True,blank=True)
    token = models.CharField(max_length=200,null=True,blank=True)
    login_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.unicode()

    def unicode(self):
        return "%s at %s" % (self.username, self.server)