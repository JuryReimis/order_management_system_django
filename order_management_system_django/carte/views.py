from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from carte.forms import DishForm
from carte.models import Dish


class AddNewDishView(generic.CreateView):
    template_name = 'carte/create-new-dish.html'
    form_class = DishForm
    success_url = reverse_lazy('carte:create_dish')


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = 'carte/dish-detail.html'

    def post(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=kwargs.get('pk'))
        title = request.POST.get('new_title', dish.title)
        price = request.POST.get('new_price', dish.price)
        form = DishForm(instance=dish, data={'price': price, 'title': title})
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return self.get(request, args, kwargs)


class GetAllDishesView(generic.ListView):
    paginate_by = 10
    context_object_name = 'dishes'
    template_name = 'carte/dish-list.html'

    def get_queryset(self):
        dishes = Dish.objects.order_by('-price')
        return dishes
