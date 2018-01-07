from django.templatetags.static import static
from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('contato/', RedirectView.as_view(url=reverse_lazy('contact'))),

    # Shorteners
    path('facebook/', RedirectView.as_view(url='https://www.facebook.com/ericpires9'), name='facebook'),
    path('github/', RedirectView.as_view(url='https://github.com/EpicEric'), name='github'),
    path('keybase/', RedirectView.as_view(url='https://keybase.io/EpicEric'), name='keybase'),
    path('linkedin/', RedirectView.as_view(url='https://www.linkedin.com/in/eric-rodrigues-pires-19231190/'), name='linkedin'),
    path('steam/', RedirectView.as_view(url='http://steamcommunity.com/id/epiceric'), name='steam'),
]
