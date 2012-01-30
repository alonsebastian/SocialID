from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ Since django's user model is hard to modify, this userprofile is easily extensible
        and although now only stores the social id and the expiration key, it can grow in the future."""
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    social_id = models.CharField(max_length=10)

    def __unicode__(self):
        return self.user.username

class idOnly(models.Model):
    """ For better performance an idOnly table was created to lookup faster"""
    social_id = models.CharField(max_length=10)
