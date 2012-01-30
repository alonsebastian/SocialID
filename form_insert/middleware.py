from search.forms import SearchForm

class SearchFormMiddleware(object):

    def process_request(self, request):
        form = SearchForm()
        return {'search_form' : form}
