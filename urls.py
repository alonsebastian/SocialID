from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'accounts.views.customLogin'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/register/$', 'accounts.views.register'),
    (r'^accounts/confirmation/(?P<activation_key>\S*)/$', 'accounts.views.confirm'),
    (r'^search/$', 'search.views.search'),
    (r'^site/modify/$', 'personal_page.views.manage'),
    (r'^$', 'static_ish.views.home'),
    (r'^who-are-we/$', 'static_ish.views.about'),
    (r'^how-it-works/$', 'static_ish.views.how'),

    (r'^facebook/login/$', 'facebook.views.login'),
    (r'^facebook/authentication_callback/$', 'facebook.views.authentication_callback'),
#    (r'^facebook_setup/(?\S+)/$', 'facebook.views.setup'),




    #SHOULD BE THE VERY LAST
    (r'^(?P<id_>\S*)/$', 'personal_page.views.personal'),

    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
