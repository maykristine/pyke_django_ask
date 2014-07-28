from django.conf.urls.defaults import *
from pyke_test.foo.views import *

urlpatterns = patterns('pyke_test.foo.views',
    (r'^species/', 'pick_species'),
    (r'^pick_form/', 'pick_form'),
)
