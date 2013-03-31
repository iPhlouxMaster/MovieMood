from django.conf.urls import patterns, include, url
from moviemood import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'^search_results/$', views.search_results, name='results'),
	#ex: /movies/10
	url(r'^movies/(?P<movie_id>\d+)/$', views.movie_detail, name='detail'),

    url(r'^classify/$', views.classify, name='classify'), #Classify (Use for maintenance purposes)
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
