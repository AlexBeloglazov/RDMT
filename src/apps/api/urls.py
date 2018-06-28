from django.urls import re_path

from api.views import Stats, Resolve, Classify


urlpatterns = [
    re_path(r'^stats$', Stats.as_view(), name='api_stats'),
    re_path(r'^doc/classify$', Classify.as_view(), name='api_classify'),
    re_path(r'^doc/resolve$', Resolve.as_view(), name='api_resolve'),
]
