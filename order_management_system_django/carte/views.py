from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from carte.forms import DishForm
from carte.models import Dish


class AddNewDishView(generic.CreateView):
    r"""Представление для создания нового блюда
    Стандартное CreateView, добавлена обработка ошибок"""
    template_name = 'carte/create-new-dish.html'
    form_class = DishForm
    success_url = reverse_lazy('carte:create_dish')

    def post(self, request, *args, **kwargs):
        try:
            method = super().post(request, *args, **kwargs)
        except Exception as err:
            messages.error(request, f"Произошла ошибка {err}")
        else:
            messages.success(request, f"Новое блюдо добавлено")
            return method
        return redirect('carte:get_all_dishes')


class DishDetailView(generic.DetailView):
    r"""Отображает страницу детальной информации о блюде
    Стандартное Detail-представление. Добавлена логика обработки post-запроса с изменением цены/названия блюда"""
    model = Dish
    template_name = 'carte/dish-detail.html'

    def post(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=kwargs.get('pk'))  # Получение объекта Dish, если не найден подъем HTTP404
        title = request.POST.get('new_title', dish.title)
        price = request.POST.get('new_price', dish.price)
        form = DishForm(instance=dish, data={'price': price, 'title': title})  # Инициализация формы
        if form.is_valid():  # Если форма валидна - сохраняем изменения и выводим сообщение об успешном сохранении
            form.save()
            messages.success(request, "Изменения успешно приняты")
        else:
            messages.warning(request, "Ошибка в заполнении формы")
        return self.get(request, args, kwargs)  # В любом случае переадресация на туже страницу


class DishDeleteView(generic.DeleteView):
    r"""Удаление блюда.
    Стандартное DeleteView, изменений нет"""
    model = Dish
    context_object_name = 'dish'
    template_name = 'carte/delete-dish-confirm.html'
    success_url = reverse_lazy('carte:get_all_dishes')


class GetAllDishesView(generic.ListView):
    r"""Вывод списка всех блюд в базе данных
    Стандартное ListView. Добавлен порядок вывод: по цене от большего к меньшему."""
    paginate_by = 9
    context_object_name = 'dishes'
    template_name = 'carte/dish-list.html'

    def get_queryset(self):
        dishes = Dish.objects.order_by('-price')
        return dishes
