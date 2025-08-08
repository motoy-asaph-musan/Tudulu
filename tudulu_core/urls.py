
# # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from users.views import home
from equipment import views as equipment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', equipment_views.home, name='home'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('users/', include('users.urls')),
    # path('equipment/', include('equipment.urls')),
    path('equipment/', include(('equipment.urls', 'equipment'), namespace='equipment')),
    path('', include('equipment.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
