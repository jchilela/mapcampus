from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
#from django.contrib import smart_selects

urlpatterns = [
    # Examples:
    url(r'^$', 'campusuhapp.views.home', name='home'),
    url(r'^floors', 'campusuhapp.views.floors', name='floors'),
    url(r'^rooms', 'campusuhapp.views.rooms', name='rooms'),
    url(r'^objects', 'campusuhapp.views.objects', name='objects'),
    url(r'^camera', 'campusuhapp.views.camera', name='camera'),
    url(r'^advancedsearch', 'campusuhapp.views.advancedsearch', name='advancedsearch'),
    url(r'^experiencia', 'campusuhapp.views.experiencia', name='experiencia'),
    url(r'^graphics', 'campusuhapp.views.graphics', name='graphics'),
    url(r'^sshmain', 'campusuhapp.views.sshmain', name='sshmain'),
    url(r'^ssh', 'campusuhapp.views.ssh', name='ssh'),
    url(r'^vgi', 'campusuhapp.views.vgi', name='vgi'),
    url(r'^sensors', 'campusuhapp.views.sensors', name='sensors'),


    



    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
