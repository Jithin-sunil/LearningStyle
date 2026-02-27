from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('Guest.urls')),
    path('guest/', include('Guest.urls')),
    path('user/', include('User.urls')),
    path('trainer/', include('Trainer.urls')),
    path('admin-panel/', include('Admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
