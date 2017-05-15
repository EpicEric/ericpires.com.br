from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^portfolio$', views.portfolio, name='portfolio'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^contato$', views.contact),
    url(r'^$', views.index, name='index'),
)
