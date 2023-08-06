import typing as ty
from abc import ABCMeta, abstractmethod

from data_access.data_record import DataRecord

Entity = ty.TypeVar('Entity')


class StorageStrategy(metaclass=ABCMeta):
    allowed_options: ty.Dict[str, str] = None

    def save(self, record: DataRecord, entity: Entity, **kwargs) -> None:
        self._check_options(record)
        options = self._select_options(record_opts=record.options, kwarg_opts=kwargs)
        self._save(record=record, entity=entity, options=options, **kwargs)

    def load(self, record: DataRecord, **kwargs) -> Entity:
        self._check_options(record)
        options = self._select_options(record_opts=record.options, kwarg_opts=kwargs)
        return self._load(record=record, options=options, **kwargs)

    def exists(self, record: DataRecord, **kwargs) -> bool:
        self._check_options(record)
        options = self._select_options(record_opts=record.options, kwarg_opts=kwargs)
        return self._exists(record=record, options=options, **kwargs)

    @abstractmethod
    def _save(self, record: DataRecord, entity: Entity, options, **kwargs):
        pass

    @abstractmethod
    def _load(self, record: DataRecord, options, **kwargs):
        pass

    @abstractmethod
    def _exists(self, record, options, **kwargs):
        pass

    @classmethod
    def _check_options(cls, record: DataRecord):
        if record.options:
            if not cls.allowed_options:
                raise ValueError(f"Options were found in \"{record.key}\" records config,"
                                 f" but options are not allowed for records of type"
                                 f" \"{record.data_source_type}:{record.data_type}\".")
            else:
                for opt_name in record.options.keys():
                    if opt_name not in cls.allowed_options:
                        raise ValueError(f"Option \"{opt_name}\" of \"{record.key}\""
                                         f" record is not allowed for records of type"
                                         f" \"{record.data_source_type}:{record.data_type}\".")

    @classmethod
    def _select_options(cls, record_opts: ty.Dict, kwarg_opts: ty.Dict):
        res_opts = {}
        if cls.allowed_options is not None:
            for opt_name, opt_val in cls.allowed_options.items():
                if kwarg_opts and (opt_name in kwarg_opts):
                    res_opts[opt_name] = kwarg_opts[opt_name]
                    del (kwarg_opts[opt_name])
                elif record_opts and (opt_name in record_opts):
                    res_opts[opt_name] = record_opts[opt_name]
                else:
                    res_opts[opt_name] = opt_val
        return res_opts
