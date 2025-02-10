from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('create-new-order/', views.CreateNewOrderView.as_view(), name="create_order"),
    path('all-orders/', views.GetAllOrdersView.as_view(), name="get_all_orders"),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name="order-detail"),
]
