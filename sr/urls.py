from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'sr.views.dashboard', name='dashboard'),
    url(r'^rate/(?P<girl_pk>\d+)/$', 'sr.views.rate', name='rate'),
    url(r'^add-girl/$', 'sr.views.girl_form', name='add_girl'),
    url(r'^edit-girl/(?P<girl_pk>\d+)/$', 'sr.views.girl_form', name='edit_girl'),
    url(r'^girl-detail/(?P<girl_pk>\d+)/$', 'sr.views.girl_detail', name='girl_detail'),
)
