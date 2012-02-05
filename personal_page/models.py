from django.db import models
from accounts.models import UserProfile

class PersonalPage (models.Model):
    """The personal page reflects all the social network in which our user participates in.
    What's more, it includes a small 'bio' field to add a user's description and since we aim
    to a worldwide user base, a location field."""

    user = models.OneToOneField(UserProfile)
    bio = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    facebook = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)
    tumblr = models.CharField(max_length=80)
    linkedin = models.CharField(max_length=100)
    personal_site = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.user.username + " personal page"
