from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

handler404 = 'homepage.error.error404'
handler500 = 'homepage.error.error500'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('homepage.urls')),
)
