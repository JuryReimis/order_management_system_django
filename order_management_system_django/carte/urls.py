from django.urls import path

from carte import views

app_name = "carte"

urlpatterns = [
    path('add-new-dish/', views.AddNewDishView.as_view(), name="create_dish"),
    path('dishes/<int:pk>/', views.DishDetailView.as_view(), name="dish_detail"),
    path('all-dishes/', views.GetAllDishesView.as_view(), name='get_all_dishes')
]
