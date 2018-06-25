from django.urls import re_path
from django.conf.urls import include

from rdmt.views import IndexView

urlpatterns = [
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^dashboard/', include('dashboard.urls')),
    re_path(r'^api/', include('api.urls')),
]
