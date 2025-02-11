from django import forms

from carte.models import Dish


class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = ['title', 'price']
