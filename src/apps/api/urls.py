from django.urls import re_path

from api.views import Upload, Classify


urlpatterns = [
    re_path(r'^doc/upload$', Upload.as_view(), name='api_upload'),
    re_path(r'^doc/predict$', Classify.as_view(), name='api_classify'),
]
