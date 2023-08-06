from dataclasses import dataclass


@dataclass
class DataRecord:
    key: str
    path: str
    data_source_type: str
    data_type: str
    options: dict = None
