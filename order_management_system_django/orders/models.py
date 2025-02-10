from django.db import models


class Order(models.Model):

    PENDING = 0
    READY = 1
    PAID = 2

    STATUS = [
        (PENDING, "В ожидании"),
        (READY, "Готов"),
        (PAID, "Оплачено")
    ]

    table_number = models.IntegerField(
        blank=False,
        verbose_name="Номер стола"
    )

    items = models.ManyToManyField(
        to='carte.Dish',
        blank=False,
        related_name="orders",
        verbose_name="Заказанные позиции"
    )

    status = models.IntegerField(
        choices=STATUS,
        verbose_name="Статус заказа"
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
