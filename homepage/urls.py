from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from . import views

urlpatterns = (
    url(r'^portfolio$', views.portfolio, name='portfolio'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^contato$', views.contact),
    url(r'^$', views.index, name='index'),

    # Shorteners
    url(r'^steam$', RedirectView.as_view(url='http://steamcommunity.com/id/epiceric'), name='steam'),
    url(r'^facebook$', RedirectView.as_view(url='https://www.facebook.com/ericpires9'), name='facebook'),
    url(r'^linkedin$', RedirectView.as_view(url='https://www.linkedin.com/in/eric-rodrigues-pires-19231190/'), name='linkedin'),
    url(r'^github$', RedirectView.as_view(url='https://github.com/EpicEric'), name='github'),
)

# Error handlers
handler400 = 'homepage.errors.bad_request'
handler403 = 'homepage.errors.permission_denied'
handler404 = 'homepage.errors.page_not_found'
handler500 = 'homepage.errors.server_error'
