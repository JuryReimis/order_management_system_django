from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('create-new-order/', views.CreateNewOrderView.as_view(), name="create_order"),
    path('all-orders/', views.GetAllOrdersView.as_view(), name="get_all_orders"),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name="order_detail"),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name="order_delete"),
    path('order/<int:pk>/change-status', views.OrderChangeStatusView.as_view(), name="order_change_status"),
    path('orders/search/', views.OrderSearchView.as_view(), name="order_search")
]
