from abc import ABC, abstractmethod
from typing import List
from app.models import CustomerEntity


class ICustomerService(ABC):
    @abstractmethod
    def create_customer(self, name: str) -> CustomerEntity: ...

    @abstractmethod
    def get_customer(self, id: int) -> CustomerEntity: ...

    @abstractmethod
    def list_customers(self) -> List[CustomerEntity]: ...

    @abstractmethod
    def delete_customer(self, id: int) -> None: ...

    @abstractmethod
    def update_customer(self, id: int, name: str) -> CustomerEntity: ...
