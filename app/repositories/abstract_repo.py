# app/repositories/abstract.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def get(self, code: str) -> Optional[T]: ...

    @abstractmethod
    def list_all(self) -> List[T]: ...

    @abstractmethod
    def delete(self, entity: T) -> None: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...
