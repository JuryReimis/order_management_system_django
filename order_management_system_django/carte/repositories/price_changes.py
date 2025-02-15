from datetime import datetime
from typing import List

from django.db.models import OuterRef, Max, F, Subquery

from carte.dto.actual_price import ActualPriceDTO
from carte.dto.dish_list_update_time import DishListUpdateTimeDTO
from carte.models import DishPriceChanges


class PriceChangesRepository:
    r"""Получение списка объектов с актуальной ценой и id блюда
    Идентичен DishPriceRepository, но задействует другой набор данных для выдачи информации

    !!!Разобраться, какой из репозиториев оставить. Задачи одни и те же."""

    @staticmethod
    def get_subquery(actual_time: datetime):
        return DishPriceChanges.objects.filter(
            dish_id=OuterRef('dish_id'),  # Связываем по dish_id
            changed__lte=actual_time  # Фильтруем по дате
        ).values('dish_id').annotate(
            max_changed=Max('changed')  # Находим максимальную дату
        ).values('max_changed')

    def _get_prices(self, ids: List[int], actual_time: datetime):
        price_changes = DishPriceChanges.objects.filter(
            dish_id__in=ids,  # Фильтруем по переданным id блюд
            changed__lte=actual_time  # Фильтруем по дате
        ).annotate(
            max_changed=Subquery(self.get_subquery(actual_time))  # Аннотируем максимальной датой
        ).filter(
            changed=F('max_changed')  # Выбираем только записи с максимальной датой
        ).values('dish_id', 'new_price')  # Выбираем только нужные поля
        return price_changes

    def get_actual_price_by_time(self, dto: DishListUpdateTimeDTO) -> List[ActualPriceDTO]:
        ids = dto.ids
        actual_time = dto.last_update
        price_changes = self._get_prices(ids, actual_time)

        return [ActualPriceDTO(
            dish_id=item['dish_id'],
            actual_price=item['new_price']
        ) for item in price_changes]
