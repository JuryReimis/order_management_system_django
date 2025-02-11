from dataclasses import dataclass


@dataclass
class SearchQueryDTO:
    r"""Data transfer object для передачи нераспарсиных запросов в сервис"""
    table: str
    status: str
