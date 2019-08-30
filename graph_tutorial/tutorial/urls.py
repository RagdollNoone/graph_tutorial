from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
  # /tutorial
  path('', views.home, name='home'),
  path('signin', views.sign_in, name='signin'),
  path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
  url(r"^calendar(?P<pIndex>[0-9]*)/$", views.calendar, name='calendar'),
]