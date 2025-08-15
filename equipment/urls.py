from django.urls import path
from . import views
from .views import CreateCheckoutSessionView, payment_success, upload_image

app_name = 'equipment'


urlpatterns = [
    path('equipment/home/', views.home, name='home'),
    # path('equipment/news/', views.post_list, name='post_list'),
    path('', views.home, name='home'),
    path('installed/', views.equipment_list, name='equipment_list'),
    path('installed/add/', views.add_equipment, name='add_equipment'),
    path('add/', views.add_equipment, name='add_equipment'),
    path('list/', views.equipment_list, name='equipment_list'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('news/', views.post_list, name='post_list'),
    path('news/create/', views.create_post, name='create_post'),
    path('equipment/create/', views.add_equipment, name='create_equipment'),
    path('news/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('news/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('upgrade/', CreateCheckoutSessionView.as_view(), name='upgrade'),
    path('payment-success/', payment_success, name='payment_success'),
    path('upload-image/', upload_image, name='upload_image'),
    path("upgrade/", views.upgrade, name="upgrade"),
    path("process-payment/", views.process_payment, name="process_payment"),
    path("upgrade/success/", views.upgrade_success, name="upgrade_success"),
    path("upgrade/cancel/", views.upgrade_cancel, name="upgrade_cancel"),
    path('cancel-subscription/', views.cancel_subscription, name='CreateCheckoutSessionView'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('upgrade/cancel/', views.upgrade_cancel, name='payment_cancel'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('upgrade/success/', views.upgrade_success, name='upgrade_success'),
    path('upgrade/cancel/', views.upgrade_cancel, name='upgrade_cancel'),
]
