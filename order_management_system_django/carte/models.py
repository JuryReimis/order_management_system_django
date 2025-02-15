from django.db import models


class Dish(models.Model):
    r"""Модель блюда.
    При сохранении проверяет, была ли изменена цена, если да,
    записывает информацию об изменении в модель DishPriceChanges"""

    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        verbose_name="Название блюда"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Цена"
    )

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        old_prices = self.prices.order_by('-changed').first()
        if old_prices:
            old_price = old_prices.new_price
        else:
            old_price = None
        if old_price != self.price:
            DishPriceChanges.objects.create(dish=self, new_price=self.price)

    def __str__(self):
        return f'{self.title} - {self.price} Р'

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class DishPriceChanges(models.Model):
    r"""Модель изменения цен.
    Хранит данные об изменении цен для каждого блюда"""

    dish = models.ForeignKey(
        to='carte.Dish',
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name="Блюдо"
    )

    new_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Новая цена"
    )

    changed = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата изменения цены"
    )

    def __str__(self):
        return f'Изменение цены для {self.dish}'

    class Meta:
        verbose_name = "Изменение цен"
        verbose_name_plural = "Изменения цен"
        ordering = ['-changed']
