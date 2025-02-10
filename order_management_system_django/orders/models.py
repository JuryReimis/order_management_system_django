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

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Общая стоимость заказа"
    )

    status = models.IntegerField(
        choices=STATUS,
        default=PENDING,
        verbose_name="Статус заказа"
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа"
    )

    def __str__(self):
        return f'Заказ для стола {self.table_number}, id {self.pk}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
