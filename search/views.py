from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from accounts.models import UserProfile
from forms import SearchForm


def search (request):
    """ View called when the form in the upper right is used to search.
        It searches through every social ID and returns a list of all the possibilities."""
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            results = UserProfile.objects.filter(social_id__icontains=form.cleaned_data['search'])
            how_many = len(results)
            results = results [:10]
            return render_to_response('search/results.html', {'results': results, 'how_many' : how_many}, context_instance=RequestContext(request))
        else: print "fuck"
    else:
        return render_to_response('search/results.html', {'invalid' : True}, context_instance=RequestContext(request))
