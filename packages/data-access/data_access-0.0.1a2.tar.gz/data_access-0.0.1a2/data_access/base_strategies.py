import os
import typing as ty
from abc import abstractmethod, ABCMeta

from data_access import StorageStrategy
from data_access.data_record import DataRecord
from data_access.storage_strategy import Entity


class FileStrategy(StorageStrategy, ty.Generic[Entity], metaclass=ABCMeta):

    # -------------------------------------- MAIN METHODS ---------------------------------------- #
    def _save(self, record: DataRecord, entity: Entity, options,
              rewrite: bool = False, create_dirs: bool = False,
              **kwargs) -> None:
        file_path = self._get_file_path(record, options, **kwargs)
        self._check_path_write(file_path=file_path,
                               rewrite=rewrite,
                               create_dirs=create_dirs)
        self._save_operation(record, entity, options, file_path, **kwargs)

    def _load(self, record: DataRecord, options, **kwargs) -> Entity:
        file_path = self._get_file_path(record, options, **kwargs)
        self._check_path_read(file_path=file_path)
        return self._load_operation(record=record, options=options, file_path=file_path, **kwargs)

    def _exists(self, record, options, **kwargs) -> bool:
        file_path = self._get_file_path(record, options, **kwargs)
        return os.path.exists(file_path)

    # ----------------------------------- METHODS TO OVERRIDE ------------------------------------ #
    @staticmethod
    def _get_file_path(record: DataRecord, options, **kwargs):
        return record.path

    @abstractmethod
    def _save_operation(self, record: DataRecord, entity: Entity, options, file_path: str, **kwargs):
        pass

    @abstractmethod
    def _load_operation(self, record: DataRecord, options, file_path: str, **kwargs):
        pass

    # ------------------------------------ PRIVATE METHODS --------------------------------------- #
    @staticmethod
    def _check_path_write(file_path, create_dirs, rewrite):
        dir_path = os.path.dirname(file_path)
        dir_exists = os.path.exists(dir_path)
        file_exists = os.path.exists(file_path)

        if file_exists and not rewrite:
            raise FileExistsError(file_path)

        if not dir_exists:
            if create_dirs:
                os.makedirs(dir_path)
            else:
                raise FileNotFoundError(dir_path)

    @staticmethod
    def _check_path_read(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)