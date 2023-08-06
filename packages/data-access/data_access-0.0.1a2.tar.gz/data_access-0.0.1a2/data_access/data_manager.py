import json
from typing import Dict

from data_access.storage_strategy import StorageStrategy
from data_access.data_record import DataRecord


class DataManager:
    data_mapping: Dict[str, DataRecord]

    def __init__(self, data_mapping=None, config_path=None):
        if data_mapping is not None:
            self.data_mapping = data_mapping
        elif config_path is not None:
            with open(config_path, encoding='utf-8') as file:
                data_records = json.load(file)
                self.data_mapping = {record["key"]: DataRecord(**record) for record in data_records}
        else:
            raise ValueError('Both data_mapping and config_path can not be None')

    def load(self, key, **kwargs):
        record = self.data_mapping[key]
        strategy = select_strategy(record)
        return strategy().load(record, **kwargs)

    def save(self, key, entity, **kwargs):
        record = self.data_mapping[key]
        strategy = select_strategy(record)
        strategy().save(record, entity, **kwargs)

    def exists(self, key, **kwargs):
        record = self.data_mapping[key]
        strategy = select_strategy(record)
        return strategy().exists(record, **kwargs)


def select_strategy(record: DataRecord):
    concrete_strategies = set()
    work = [StorageStrategy, ]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in concrete_strategies:
                concrete_strategies.add(child)
                work.append(child)

    strategies = {
        (child.data_source_type, child.data_type): child
        for child in concrete_strategies
        if hasattr(child, "data_source_type") and hasattr(child, "data_type")
    }

    try:
        return strategies[(record.data_source_type, record.data_type)]
    except KeyError:
        raise KeyError(f'Unknown combination of data source and data type:'
                       f' {record.data_source_type, record.data_type}')
