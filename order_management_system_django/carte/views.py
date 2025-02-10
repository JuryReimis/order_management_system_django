from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from carte.forms import AddNewDishForm
from carte.models import Dish


class AddNewDishView(generic.CreateView):
    template_name = 'carte/create-new-dish.html'
    form_class = AddNewDishForm
    success_url = reverse_lazy('carte:create_dish')


class GetAllDishesView(generic.ListView):
    paginate_by = 10
    context_object_name = 'dishes'
    template_name = 'carte/dish-list.html'

    def get_queryset(self):
        dishes = Dish.objects.order_by('-price')
        return dishes

