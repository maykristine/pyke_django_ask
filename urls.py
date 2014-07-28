from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^foo/', include('pyke_django_ask.foo.urls')),

)
