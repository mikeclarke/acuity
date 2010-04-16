from django.conf.urls.defaults import *
from django.contrib import admin
from views import dirlist
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^browse$', dirlist),
    (r'^admin/', include(admin.site.urls)),
)
