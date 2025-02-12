from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DishListUpdateTimeDTO:

    ids: List[int]
    last_update: datetime
