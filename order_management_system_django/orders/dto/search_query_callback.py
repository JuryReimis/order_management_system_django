from dataclasses import dataclass
from typing import List

from django.db.models import Q


@dataclass
class SearchQueryCallbackDTO:
    r"""Data transfer object для передачи получившихся фильтров"""

    filter: Q
    errors: List[str]

