import urllib
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)

    if user.is_anonymous():
        print "aca vaaaaaaaaa: "
        print code
        #we have to set this user up
        url = reverse('facebook_setup')
        url += "?code=%s" % code

        return redirect(url)

    else:
        auth_login(request, user)

        #figure out where to go after setup
        url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
        print "url mother fucker: " + url
        print "code mother fucker: "
        print code
        return redirect(url)

def setup(request):
    print "WTF is going oooon!!!!"
    return HttpResponseRedirect("/")
