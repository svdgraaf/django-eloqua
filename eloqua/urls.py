from django.conf.urls.defaults import patterns, include, url
from .views import LandingPageView

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)-?(?P<slug>[a-zA-Z0-9-_]+)?/?$', LandingPageView.as_view(),  name='eloqua:landing_page'),
)
