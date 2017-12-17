from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^request/', views.RequestProccessingView.as_view(), name='request-processing'),

    url(r'^view/', views.ViewResultsView.as_view(), name='view-results'),
]
