from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def home (request):
    """ Almost static views that do not have any processing (but exists to show the result of
    context processor work and others. """
    return render_to_response('static_ish/home.html', {}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('static_ish/about.html', {}, context_instance=RequestContext(request))

def how (request):
    return render_to_response('static_ish/how.html', {}, context_instance=RequestContext(request))

#def stories (request):
#    return render_to_response('static_ish/stories.html', {}, context_instance=RequestContext(request))
