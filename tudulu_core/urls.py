
# # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from users.views import home
from equipment import views as equipment_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', equipment_views.home, name='home'),

    # Login page
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # User-related URLs
    # path('users/', include('users.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),


    # Equipment URLs with namespace
    path('equipment/', include(('equipment.urls', 'equipment'), namespace='equipment')),
    path('equipment/', include('equipment.urls', namespace='equipment')),

    # Default Django auth URLs (password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
