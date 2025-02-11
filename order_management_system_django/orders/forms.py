from django import forms
from django.db import IntegrityError

from orders.models import Order


class CreateNewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']


class UpdateOrderItemsForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['items']
