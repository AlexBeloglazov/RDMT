from django.views.generic import RedirectView


class IndexView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'dashboard_index'
