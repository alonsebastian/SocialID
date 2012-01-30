from search.forms import SearchForm

def addSearchForm(request):
    """ Generates the search form displayed in the upper right corner. """
    form = SearchForm()
    return {'search_form' : form}
