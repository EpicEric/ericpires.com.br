from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('homepage.urls')),
)

# Error handlers
handler400 = 'homepage.errors.bad_request'
handler403 = 'homepage.errors.permission_denied'
handler404 = 'homepage.errors.page_not_found'
handler500 = 'homepage.errors.server_error'
