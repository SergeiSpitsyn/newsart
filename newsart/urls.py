"""
Definition of urls for newsart.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.views.generic.base import RedirectView                                          # add a favicon (1/3)
import app.forms
import app.views

# Enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

# Configuring access to uploaded files (1/2):
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

favicon_view = RedirectView.as_view(url='/static/app/content/favicon.ico', permanent=True)  # add a favicon (2/3)

urlpatterns = [
    # Examples:
    url(r'^favicon\.ico$', favicon_view),                                   # add a favicon (3/3)
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^links$', app.views.links, name='links'),
    url(r'^pool$', app.views.pool, name='pool'),
    url(r'^blog$', app.views.blog, name='blog'),                            # add a page with list of posts
    url(r'^(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'),      # implements individual post pages and 'Читать далее' button
    url(r'^registration$', app.views.registration, name='registration'),
    url(r'^videopost$', app.views.videopost, name='videopost'),
    url(r'^newpost$', app.views.newpost, name='newpost'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Войти',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

# Configuring access to uploaded files (2/2):
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()