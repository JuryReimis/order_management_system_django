from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatesQueryDTO:
    r"""DTO для передачи начальной и конечной даты дял какой-то выборки"""

    start_date: datetime
    end_date: datetime
