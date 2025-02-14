from django.urls import path

from carte.api.v1 import views

urlpatterns = [
    path('api/v1/dishes/create/', views.CreateDishAPIView.as_view(), name='create_dish_api'),
    path('api/v1/dishes/', views.GetDishesAPIView.as_view(), name='get_dish_list_api'),
    path('api/v1/dishes/<int:pk>/', views.GetDishDetailAPIView.as_view(), name='get_dish_detail_api'),
    path('api/v1/dishes/<int:pk>/update/', views.UpdateDishAPIView.as_view(), name='update_dish_api'),
    path('api/v1/dishes/<int:pk>/delete/', views.DeleteDishAPIView.as_view(), name='delete_dish_api'),
]
