from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new-user/', views.CreateUserView.as_view(), name='new-user'),

    url(r'^auth/', views.LoginView.as_view(), name='login'),
]
