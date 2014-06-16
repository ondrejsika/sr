from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('sr.urls', namespace='sr')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'form.html', }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html', }, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
