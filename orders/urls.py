from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Giao diện khách hàng
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.order_success, name='success'),
    path('history/', views.order_history, name='history'),
    path('detail/<str:order_number>/', views.order_detail, name='detail'),

    # Giao diện quản trị Admin
    path('management/orders/', views.admin_order_list, name='admin_order_list'),
    path('management/orders/<str:order_number>/', views.admin_order_detail, name='admin_order_detail'),
]
