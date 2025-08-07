from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('home/', views.home, name='equipment-home'),
    path('installed/', views.equipment_list, name='equipment-list'),
    path('installed/add/', views.add_equipment, name='add-equipment'),
    # path('', views.home, name='home'),
    path('add/', views.add_equipment, name='add-equipment'),
    path('list/', views.equipment_list, name='equipment-list'),
    path('export/excel/', views.export_excel, name='export-excel'),
    path('export/pdf/', views.export_pdf, name='export-pdf'),
    path('news/', views.post_list, name='post-list'),
    path('news/create/', views.create_post, name='create-post'),
    path('news/like/<int:post_id>/', views.toggle_like, name='toggle-like'),
    path('news/comment/<int:post_id>/', views.add_comment, name='add-comment'),
]
