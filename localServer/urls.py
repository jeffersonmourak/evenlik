from django.conf.urls import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','evenlik.views.index'),
    url(r'^confirm/(?P<hash>\S+)/$','evenlik.views.confirm'),
    url(r'^admin/$','evenlik.admin.subscribers'),
    url(r'^admin/checkin/$','evenlik.admin.checkin'),
    url(r'^login/$','evenlik.admin.login'),
    url(r'^admin/editor/$','evenlik.admin.edit_event'),
    url(r'^admin/mail/$','evenlik.admin.massMail'),
    url(r'^admin/logout/$','evenlik.admin.logout'),
    url(r"^certificate/(?P<hash>\S+)/$", 'evenlik.admin.generatePDF'),
    # url(r'^$', 'localServer.views.home', name='home'),
    # url(r'^localServer/', include('localServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r"^media/(?P<path>.*)$", 'django.views.static.serve',{'document_root' : settings.MEDIA_ROOT, 'show_indexes' : True}),
)
