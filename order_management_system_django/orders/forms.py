from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

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


class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(
        label="Начальная дата",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        validators=[
            MinValueValidator(limit_value=timezone.make_aware(datetime(2000, 1, 1)))
        ]
    )
    end_date = forms.DateTimeField(
        label="Конечная дата",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        validators=[
            MinValueValidator(limit_value=timezone.make_aware(datetime(2000, 1, 1)))
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Начальная дата должна быть меньше или равна конечной дате.")

        return cleaned_data
