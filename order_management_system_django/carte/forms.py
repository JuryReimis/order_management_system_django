from django import forms

from carte.models import Dish


class DishForm(forms.ModelForm):
    r"""Стандартная ModelForm для модели Dish"""
    class Meta:
        model = Dish
        fields = ['title', 'price']
