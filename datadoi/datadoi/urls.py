from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'datadoi.views.home', name='home'),
    # url(r'^datadoi/', include('datadoi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^registry/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^registry/', include(admin.site.urls)),

    url(r'^doi/(?P<slug>[-\w]+)/$', 'datacite.views.detail'),
    url(r'^xml/\w+/view/landing-2\.2\.xsl$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^xml/(?P<slug>[-\w]+)/(?P<disposition>[\w]+)/$', 'datacite.views.xml'),
    url(r'^queue/$', 'datacite.views.queue'),
    url(r'^$', 'datacite.views.index'),
)
