from django.db import models


class Dish(models.Model):

    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        verbose_name="Название блюда"
    )

    price = models.PositiveIntegerField(
        blank=False,
        verbose_name="Цена"
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
