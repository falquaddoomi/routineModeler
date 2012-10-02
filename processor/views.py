from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))

def auth(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))

def tasks(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))

def traces(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))

def models(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))

def summary(request):
    return render_to_response('modeler/subviews/home.html', {}, context_instance=RequestContext(request))


# =================================================
# = OHMAGE AUTH STUFF BELOW
# =================================================

from ohmagekit.clients.ohmage import OhmageApi

def ohmage_login(request):
    # query to authenticate the user based on their inputted data from the form
    try:
        api = OhmageApi(settings.OHMAGE_SERVER)
        api.login(request.POST['ohmage_username'], request.POST['ohmage_password'])
    except OhmageApi.OhmageApiException as ex:
        # authentication failed, make up a friendly message about it
        ctx = {
            'ohmage_last_username': request.POST['ohmage_username'],
            'ohmage_auth_errors': ex.errors
        }
        return render_to_response('index.html', build_context(request, ctx), context_instance=RequestContext(request))

    # lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username=api.auth_username)
    except User.DoesNotExist:
        user = User.objects.create_user(api.auth_username,
            '%s@ohmage.com' % api.auth_username, request.POST['ohmage_password'])

    # attempt to access their existing profile, or create a new one if it doesn't exist
    try:
        profile = user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile()
        profile.user = user
        # ensure that the user's new profile is in the db
        profile.save()

    # attempt to access their existing ohmage account, or create a new one if it doesn't exist
    try:
        ohmage_acct = profile.ohmageaccount
    except OhmageAccount.DoesNotExist:
        ohmage_acct = OhmageAccount()
        ohmage_acct.profile = profile
        print "Created ohmage account, associated with user's profile..."

    # save their credentials with their account
    ohmage_acct.server = api.server
    ohmage_acct.username = api.auth_username
    ohmage_acct.hashedpass = api.auth_hashedpass
    ohmage_acct.token = api.auth_token
    ohmage_acct.login_date = datetime.now()
    ohmage_acct.save()

    # Authenticate the user and log them in using Django's pre-built
    # functions for these things.
    user = authenticate(username=api.auth_username, password=request.POST['ohmage_password'])
    login(request, user)

    # ok, i guess that worked?
    return redirect('processor:auth')


@login_required
def ohmage_unlink(request):
    # wipe their entire profile
    try:
        profile = request.user.get_profile()
        profile.delete()
    except Profile.DoesNotExist:
        pass

    logout(request)
    return redirect('processor:auth')


@login_required
def ohmage_logout(request):
    # just log them out
    logout(request)
    return redirect('processor:auth')