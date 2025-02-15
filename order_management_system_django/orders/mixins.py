from carte.repositories.dish import DishRepository
from carte.repositories.price_changes import PriceChangesRepository
from orders.dto.order import OrderDTO
from orders.dto.search_query import SearchQueryDTO
from orders.models import Order
from orders.repositories.order import OrderRepository
from orders.services.compile_order_filter import CompileOrderFilterService
from orders.services.get_detail_order_context import GetDetailOrderContextService


class GetOrdersListMixin:

    def get(self, request, *args, **kwargs):
        table = str(request.GET.get('table'))
        status = str(request.GET.get('status'))
        service = CompileOrderFilterService()
        query = SearchQueryDTO(table=table, status=status)
        callback = service.execute(query)
        filter_opt = callback.filter
        self.kwargs['filter_opt'] = filter_opt
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        filter_opt = self.kwargs.pop('filter_opt', None)
        order_by = self.request.GET.get('sort')
        if not order_by:
            order_by = '-created'
        if filter_opt is not None:
            orders = Order.objects.filter(filter_opt).order_by(order_by).prefetch_related('items')
        else:
            orders = Order.objects.all().order_by(order_by)
        return orders


class GetOrderDetailMixin:

    def get_object(self):
        dto = OrderDTO(
            order_id=self.kwargs['pk'],
            status_display=None,
            updated=None,
            table_number=None,
            status=None,
            items=None,
            total_price=None
        )
        order_repository = OrderRepository
        dish_repository = DishRepository
        price_changes_repository = PriceChangesRepository
        service = GetDetailOrderContextService(order_repository=order_repository, dish_repository=dish_repository,
                                               price_changes_repository=price_changes_repository)
        obj = service.execute(order_dto=dto)
        return obj
