from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from personal_page.models import PersonalPage
from personal_page.forms import PersonalPageForm
from accounts.models import UserProfile

def personal(request, id_): #send id from url.py as argument
    """ Return the personal page requested. In case none was found with such an ID,
        no 404 code is returned, but the message that no such personal page has been created"""
    id_ = id_.lower()
    user = UserProfile.objects.filter(social_id = id_)
    site = PersonalPage.objects.filter(user = user)
    context_instance = RequestContext(request)
    editable = False
    if request.user.is_authenticated():
        for dictionary in context_instance:
            if 'id_' in dictionary: 
                if dictionary['id_'] == id_:
                    editable = True
                    break
    if user and site:
        site = site[0]
        no_bio = edit_button = False
        if site.bio == "":
            no_bio = True
        if request.user == user[0].user:
            edit_button = True
        return render_to_response("personal_page/general.html", {'site' : site, 'no_bio' : no_bio, 'edit_button' : edit_button, 'editable' : editable},
                                  context_instance)
    return render_to_response("personal_page/general.html", {'not_found' : True, 'editable' : editable}, context_instance)



@login_required
def manage (request):
    """In case the request is a get, a form to modify the personal page is shown.
        If the login user had personal page before, the form is filled with the field's
        information in the database.
        In case the request is post, the form is validated and the database updated."""
    if not request.POST:
        form = PersonalPageForm()
        profile = UserProfile.objects.get(user = request.user)
        old = PersonalPage.objects.filter(user = profile)
        if old:
            old = old [0]
            form.initial = {'bio' : old.bio, 'facebook': old.facebook, 'location': old.location, 'email': old.email, 'linkedin' : old.linkedin, 'twitter' : old.twitter,
                            'tumblr' : old.tumblr, 'personal_site': old.personal_site}
        return render_to_response("personal_page/modify.html", {'form':form}, context_instance=RequestContext(request))
    else:
        form = PersonalPageForm(request.POST)
        profile = UserProfile.objects.get(user = request.user)
        old = PersonalPage.objects.filter(user = profile)
        if old and form.is_valid():
            old = old[0]                #Bio: (u"I'm saraza men!",)     WTF
            old.bio = form.cleaned_data['bio']
            old.location = form.cleaned_data['location']
            old.email = form.cleaned_data['email']
            old.linkedin = form.cleaned_data['linkedin']
            old.facebook = linkMaker(form.cleaned_data['facebook'])
            old.twitter = twitterizer(form.cleaned_data['twitter'])
            old.tumblr = linkMaker(form.cleaned_data['tumblr'])
            old.personal_site = linkMaker(form.cleaned_data['personal_site'])
            address = "/" + profile.social_id + "/"
            old.save()
            return redirect(address)  #aca va el home
        if form.is_valid():
            page = PersonalPage(user = profile,
                                bio = form.cleaned_data['bio'],
                                location = form.cleaned_data['location'],
                                email = form.cleaned_data['email'],
                                linkedin = linkMaker(form.cleaned_data['linkedin']),
                                facebook = linkMaker(form.cleaned_data['facebook']),
                                twitter = twitterizer(form.cleaned_data['twitter']),
                                tumblr = linkMaker(form.cleaned_data['tumblr']),
                                personal_site = linkMaker(form.cleaned_data['personal_site']))
            page.save()
            address = "/" + profile.social_id + "/"
            return redirect(address)  #aca va el home
        else:
            form = PersonalPageForm()
        return render_to_response("personal_page/modify.html", {'form':form}, context_instance=RequestContext(request))

def linkMaker(string):
    """ Some users would give the full URL to their online profiles (facebook, linkedin, etc).
        Other didn't. Because of this every URL goes through this simple filter to make sure it
        is a link."""
    if string == "": return ""
    if "http://" not in string.lower():
        string = "http://" + string
        print string
        return string
    else: return string

def twitterizer (string):
    """ Some users would use the URL to their twitter profile and some used their user
    '@myCoolAccount'. Due to this, this function normalizes everything to a link displayable
    in the personal page."""
    if string and string[0] == "@":
        return "https://twitter.com/#!/" + string [1:]
    else:
        return linkMaker(string)
