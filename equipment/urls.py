from django.urls import path
from . import views
from .views import CreateCheckoutSessionView, payment_success, upload_image

app_name = 'equipment'

urlpatterns = [
    # General app views
    path('', views.home, name='home'),
    path('upload-image/', views.upload_image, name='upload_image'),

    # Payment-related views
    path('upgrade/', views.upgrade, name='upgrade'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.upgrade_cancel, name='upgrade_cancel'),
    # Note: The stripe_webhook URL should be configured separately in your project's main urls.py
    # path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),

    # Equipment-related views
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/list/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/rent/<int:equipment_id>/', views.rent_equipment, name='rent_equipment'),
    path('equipment/<int:id>/edit/', views.edit_equipment, name='edit_equipment'),
    # path('equipment/<int:id>/delete/', views.delete_equipment, name='delete_equipment'),
    path('equipment/<int:pk>/delete/', views.delete_equipment, name='delete_equipment'),

    # Data export views
    path('equipment/export/excel/', views.export_excel, name='export_excel'),
    path('equipment/export/pdf/', views.export_pdf, name='export_pdf'),

    # Post-related views
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/like/<int:pk>/', views.like_post, name='like_post'),
    # Notifications
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/<int:pk>/read/", views.mark_notification_as_read, name="mark_notification_as_read"),

]

# urlpatterns = [
#     path('equipment/home/', views.home, name='home'),
#     # path('equipment/news/', views.post_list, name='post_list'),
#     path('', views.home, name='home'),
#     path('installed/', views.equipment_list, name='equipment_list'),
#     path('installed/add/', views.equipment_add, name='equipment_add'),
#     path('add/', views.equipment_add, name='equipment_add'),
#     path('list/', views.equipment_list, name='equipment_list'),
#     path('export/excel/', views.export_excel, name='export_excel'),
#     path('export/pdf/', views.export_pdf, name='export_pdf'),
#     path('news/', views.post_list, name='post_list'),
#     path('news/create/', views.create_post, name='create_post'),
#     path('equipment/create/', views.add_equipment, name='create_equipment'),
#     path('news/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
#     path('news/comment/<int:post_id>/', views.add_comment, name='add_comment'),
#     path('post/<int:pk>/', views.post_detail, name='post_detail'),
#     path('post/<int:pk>/like/', views.like_post, name='like_post'),
#     path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
#     path('create-post/', views.create_post, name='create_post'),
#     path('upgrade/', CreateCheckoutSessionView.as_view(), name='upgrade'),
#     path('payment-success/', payment_success, name='payment_success'),
#     path('upload-image/', upload_image, name='upload_image'),
#     path("upgrade/", views.upgrade, name="upgrade"),
#     path("process-payment/", views.process_payment, name="process_payment"),
#     path("upgrade/success/", views.upgrade_success, name="upgrade_success"),
#     path("upgrade/cancel/", views.upgrade_cancel, name="upgrade_cancel"),
#     path('cancel-subscription/', views.cancel_subscription, name='CreateCheckoutSessionView'),
#     path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
#     path('payment-success/', views.payment_success, name='payment_success'),
#     path('upgrade/cancel/', views.upgrade_cancel, name='payment_cancel'),
#     path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
#     path('upgrade/', views.upgrade, name='upgrade'),
#     path('upgrade/success/', views.upgrade_success, name='upgrade_success'),
#     path('upgrade/cancel/', views.upgrade_cancel, name='upgrade_cancel'),
#     path('news/', views.create_post, name='create_post'),
#     path('news/<int:post_id>/', views.post_detail, name='post_detail'),
#     # This is the new URL pattern for editing a post
#     path('news/<int:post_id>/edit/', views.edit_post, name='edit_post'),
#     path('news/<int:post_id>/delete/', views.delete_post, name='delete_post'),
#     path('rent/<int:equipment_id>/', views.rent_equipment, name='rent_equipment'),
#     path('upgrade/', views.upgrade, name='upgrade'),
# ]

