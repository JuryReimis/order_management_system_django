from typing import List

from django.db.models import Q

from orders.dto.search_query import SearchQueryDTO
from orders.dto.search_query_callback import SearchQueryCallbackDTO
from orders.models import Order


class CompileOrderFilterService:
    r"""Формирует фильтр для поиска по заказам
    На вход поступает объект со строками.
    В строке могут быть перечислены несколько столов и несколько таблиц
    Должны быть разделены запятыми"""

    def __init__(self):
        self.errors = []

    def _add_value_table_error(self, text_error):
        text = f"Произошла ошибка при считывании номера стола из запроса\n{text_error}"
        self.errors.append(text)

    def _compile_table_number_filter(self, tables: List[int]) -> Q:
        r"""Компиляция фильтра по списку номеров столов"""
        if tables:
            return Q(table_number__in=tables)
        return Q()

    def _parse_str_to_int_list(self, query: str) -> list | List[int]:
        r"""Парсим строку со списком столов на список int значений """
        try:
            return list(map(int, query.replace(' ', '').split(',')))
        except ValueError:
            self._add_value_table_error(f"Запрос {query} не может быть превращен в список номеров")
            return []

    def _compile_status_filter(self, status_list: List[int]):
        r"""Компиляция фильтра на основе списка статусов"""
        if status_list:
            return Q(status__in=status_list)
        return Q()

    def _check_valid_status(self, status_list: List[str]) -> list[int] | None:
        valid_status_list = []
        for status in status_list:
            valid = Order.get_status_db(status.lower().strip())
            if valid is not None:
                valid_status_list.append(valid)
        return valid_status_list

    def _parse_status_in_list(self, status: str) -> List[str]:
        r"""Парсим строку статусов на список статусов"""
        status_list = status.split(',')
        return status_list

    def execute(self, search_query: SearchQueryDTO) -> SearchQueryCallbackDTO:
        table = search_query.table
        status = search_query.status
        filter_opt = Q()
        if table is not None:
            table_numbers = self._parse_str_to_int_list(table)
            filter_opt &= self._compile_table_number_filter(table_numbers)
        if status is not None:
            status_list = self._parse_status_in_list(status)
            valid_status_list = self._check_valid_status(status_list)
            filter_opt &= self._compile_status_filter(valid_status_list)

        callback = SearchQueryCallbackDTO(
            filter=filter_opt,
            errors=self.errors
        )
        return callback
