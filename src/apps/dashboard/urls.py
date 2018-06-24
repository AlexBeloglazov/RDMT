from django.urls import re_path

from dashboard.views import IndexView, TrainView, ClassifyView


urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='dashboard_index'),
    re_path(r'^train$', TrainView.as_view(), name='dashboard_train'),
    re_path(r'^train$', ClassifyView.as_view(), name='dashboard_classify'),

]
