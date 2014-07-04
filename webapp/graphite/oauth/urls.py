from django.conf.urls.defaults import *

urlpatterns = patterns('graphite.oauth',
  ('^login/?$', 'oauth.authorize'),
  ('^callback/?$', 'oauth.callback'),
  ('^logout/?$', 'views.logoutView'),
)
