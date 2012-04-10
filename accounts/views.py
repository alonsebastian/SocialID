import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile, idOnly
from accounts.forms import RegistrationForm, LoginForm, changePassForm
from personal_page.models import PersonalPage
from search.forms import SearchForm


def register(request):
    """ If the request is GET, a form is displayed with the necessary fields to register a new user.
        Otherwise, the form is validated and checked if there is another user with the same username
        or email. IF there is not a new user (django.contrib.auth) is created and a UserProfile that
        is related to the user is also created.
        A link is sent to the user's email to activate the account, which will expire in 2 days from
        registration."""

    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('accounts/register.html', {'has_account': True}, context_instance=RequestContext(request))
    if request.POST:
        form = RegistrationForm(request.POST)
        form_b = form
        if form.is_valid() and len(User.objects.filter(username = form.cleaned_data['username'])) == 0:
            if len(User.objects.filter(email = form.cleaned_data['email'])) > 0:
                email_in_use = True
                return render_to_response('accounts/register.html', {'form': form, 'email_in_use' : email_in_use}, context_instance=RequestContext(request))
            #There is no user with that email and username
            # Save the user
            new_user = User.objects.create_user(form.cleaned_data['username'],
                            form.cleaned_data['email'],
                            form.cleaned_data['password1'])
            new_user.is_active = False
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            
            # Build the activation key for their account
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #build the social salt
            existing_ids = idOnly.objects.all()
            newid = idOnly()
            id_salt = sha.new(salt+new_user.first_name+new_user.email).hexdigest()[:8]
            newid.social_id = id_salt
            #In case that social ID already existed, a new hash is created adding a random number.
            while newid in existing_ids:
                newid.social_id = sha.new(str(random.random())+new_user.first_name+new_user.email).hexdigest()[:8]

            #once a non existing id is created, it is saved
            newid.save()

            # Create and save their profile
            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires,
                                      social_id = id_salt)
            new_profile.save()
            
            # Send an email with the confirmation link
            email_subject = 'Your new Social ID confirmation'
            email_body = "Hello, %s, and thanks for registering a new Social ID!\nYour new Social ID is: %s\n\nTo activate your account, click this link within 48 hours:\n\nhttp://social-id.com.ar/accounts/confirmation/%s\n\nRemember your password is: %s" % (new_user.username, id_salt, new_profile.activation_key, form.cleaned_data['password1'])
            send_mail(email_subject,
                      email_body,
                      'noreply@social-id.com.ar',
                      [new_user.email])
            #created

            #Create initial Personal Page
            initial = PersonalPage (user = new_profile,
                                    email = new_user.email,
                                    bio = new_user.first_name + " " + new_user.last_name + "\n No more data available.")
            initial.save()
            #minimal Personal Page created


            return render_to_response('accounts/register.html', {'created': True}, context_instance=RequestContext(request))
        elif form.is_valid():
            #form is valid, but username's taken
            return render_to_response('accounts/register.html', {'form': form, 'name_in_use' : True}, context_instance=RequestContext(request))
        else:
            #form was not valid, some fields must have been empty
            form = RegistrationForm()
            return render_to_response('accounts/register.html', {'form': form, 'empty' : True}, context_instance=RequestContext(request))
    else:
    #GET request
        form = RegistrationForm()
    return render_to_response('accounts/register.html', {'form': form}, context_instance=RequestContext(request))




def confirm(request, activation_key):
    """Every activation link (sent to email) leads to this view. It is this view's job to validate the accounts
    while check if the link has not expired."""

    if request.user.is_authenticated():
        return render_to_response('accounts/confirm.html', {'has_account': True}, context_instance=RequestContext(request))
    #Lookup userprofile by activation key
    user_profile = UserProfile.objects.filter(activation_key=activation_key)

    #if key does not match one unique user
    if len(user_profile) != 1:
        return render_to_response('accounts/confirm.html', {'not_found': True}, context_instance=RequestContext(request))

    #if key has expired
    if user_profile[0].key_expires < datetime.datetime.today():
        return render_to_response('accounts/confirm.html', {'expired': True}, context_instance=RequestContext(request))

    #if everything is alright
    user_account = user_profile[0].user
    user_account.is_active = True
    user_account.save()
    return render_to_response('accounts/confirm.html', {'success': True}, context_instance=RequestContext(request))



def customLogin(request):
    """ This view is meant to replace django.contrib.auth login. It allows us to add custom features
    (eg: redirect to personal page edit when logged in for first time). """
    form = LoginForm()
    if request.POST:
        #Authenticate the data in the form
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:    #user exists
            if user.is_active:
                #Log user in, get their profile and check if it has a personal page
                login(request, user)
                profile = UserProfile.objects.get(user = user)
                page = PersonalPage.objects.get(user = profile)
                if page and page.bio != (user.first_name + " " + user.last_name + "\n No more data available."):
                    return redirect('/')
                else:
                    return render_to_response('accounts/welcome.html', {}, context_instance=RequestContext(request))
            else:
                return render_to_response('accounts/confirm.html', {'invalid': True, 'form' : form}, context_instance=RequestContext(request))
        else:
             return render_to_response('registration/login.html', {'invalid': True, 'form' : form}, context_instance=RequestContext(request))
    else:
        return render_to_response('registration/login.html', {'form' : form}, context_instance = RequestContext(request))


@login_required
def changePassword (request):
    if request.POST:
        form = changePassForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                request.user.set_password(form.cleaned_data['password1'])
                request.user.save()
                return redirect("/")
            else:
                form = changePassForm()
                return render_to_response("accounts/changepass.html", {'form' : form, 'samepass' : True}, context_instance = RequestContext(request))
    else:
        form = changePassForm()
        return render_to_response("accounts/changepass.html", {'form' : form}, context_instance = RequestContext(request))
