from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import CustomerEntity
from app.repositories.abstract_repo import AbstractRepository


class SqlCustomerRepository(AbstractRepository[CustomerEntity]):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, entity: CustomerEntity) -> CustomerEntity:
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def get(self, code: str) -> CustomerEntity | None:
        stmt = select(CustomerEntity).where(CustomerEntity.code == code)  # type: ignore
        return (await self._session.execute(stmt)).scalars().first()

    async def list_all(self) -> list[CustomerEntity]:
        return (
            (await self._session.execute(select(CustomerEntity)))
            .scalars()
            .all()
        )  # type: ignore

    async def delete(self, entity: CustomerEntity) -> None:
        await self._session.delete(entity)

    async def update(self, entity: CustomerEntity) -> CustomerEntity:
        await self._session.merge(entity)
        await self._session.flush()
        return entity
