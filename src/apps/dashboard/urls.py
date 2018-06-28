from django.urls import re_path

from dashboard.views import IndexView, StatsView, ResolveView


urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='dashboard_index'),
    re_path(r'stats$', StatsView.as_view(), name='dashboard_stats'),
    re_path(r'^resolve/(?P<id>\d+)$', ResolveView.as_view(), name='dashboard_resolve')
]
