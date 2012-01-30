from search.forms import SearchForm

class SearchFormMiddleware(object):

    def process_request(self, request):
        form = SearchForm()
        print "salio!!!"
        return {'search_form' : form}
