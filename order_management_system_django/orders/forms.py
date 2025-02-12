from django import forms
from django.db import IntegrityError

from orders.models import Order, OrderItems


class CreateNewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']


class UpdateOrderItemsForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['items']


class UpdateQuantityForm(forms.ModelForm):
    dish_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = OrderItems
        fields = ['dish_id', 'quantity']
