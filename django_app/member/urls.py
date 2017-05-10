from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^signin/facebook/$', views.signin_facebook, name='signin_facebook')
]
