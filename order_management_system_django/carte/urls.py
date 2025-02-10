from django.urls import path

from carte import views

app_name = "carte"

urlpatterns = [
    path('add-new-dish/', views.AddNewDishView.as_view(), name="create_dish"),
    path('all-dishes/', views.GetAllDishesView.as_view(), name='get_all_dishes')
]
