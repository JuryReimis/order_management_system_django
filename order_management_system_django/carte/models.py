from django.db import models


class Dish(models.Model):

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

    def __str__(self):
        return f'{self.title} за {self.price} Р'

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class DishPriceChanges(models.Model):

    dish = models.ForeignKey(
        to='carte.Dish',
        on_delete=models.CASCADE,
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
