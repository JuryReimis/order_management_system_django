from django.urls import path

from orders.api.v1 import views

urlpatterns = [
    path('api/v1/orders/create/', views.CreateOrderAPIView.as_view(), name="create_order_api"),
    path('api/v1/orders/get-orders/', views.GetOrdersListAPIView.as_view(), name="get_orders_list_api"),
    path('api/v1/orders/<int:pk>/', views.GetOrderDetailAPIView.as_view(), name="get_order_detail_api"),
    path('api/v1/orders/<int:pk>/update/', views.UpdateOrderItemsAPIView.as_view(), name="update_order_items_api"),
    path('api/v1/orders/<int:pk>/delete/', views.DeleteOrderAPIView.as_view(), name="delete_order_api")
]
