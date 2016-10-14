from django.conf.urls import url
from django.contrib import admin
from feeds.views import home, event, comment


urlpatterns = [
    url(r'^$', home),
    url(r'^comment/$', comment), # AjaxHandler
    url(r'^event/(?P<slug>[^/]+)/$', event),
    url(r'^admin/', admin.site.urls),
]
