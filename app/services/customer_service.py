from typing import List
from xml.dom import NotFoundErr

from cachetools import TTLCache
from app.models import CustomerEntity
from app.repositories.abstract_repo import AbstractRepository


class CustomerService:
    def __init__(
        self,
        repo: AbstractRepository[CustomerEntity],
        *,
        cache_maxsize=128,
        cache_ttl=300,
    ):
        self._repo = repo

        # a simple LRU+TTL cache mapping code → CustomerEntity
        self._get_cache = TTLCache(maxsize=cache_maxsize, ttl=cache_ttl)
        self._list_cache = TTLCache(maxsize=1, ttl=cache_ttl)

    async def create_customer(self, code: str, name: str) -> CustomerEntity:
        cust = CustomerEntity(code=code, name=name)
        created = await self._repo.add(cust)

        # insert into get_cache immediately
        self._get_cache[code] = created
        # invalidate list cache
        self._list_cache.clear()
        return created

    async def get_customer(self, code: str) -> CustomerEntity:
        # try cache first
        if code in self._get_cache:
            return self._get_cache[code]

        # miss → hit the repo
        cust = await self._repo.get(code)  # type: ignore
        if not cust:
            raise NotFoundErr(f"code={code} not found")

        # store in cache
        self._get_cache[code] = cust
        return cust

    async def list_customers(self) -> List[CustomerEntity]:
        # we only ever cache the full list under a single key
        if "all" in self._list_cache:
            return self._list_cache["all"]

        all_customers = await self._repo.list_all()  # type: ignore
        self._list_cache["all"] = all_customers
        return all_customers

    async def delete_customer(self, code: str) -> None:
        cust = await self.get_customer(code)
        await self._repo.delete(cust)  # type: ignore

        # evict deleted and refresh list
        self._get_cache.pop(code, None)
        self._list_cache.clear()

    async def update_customer(self, code: str, name: str) -> CustomerEntity:
        cust = await self.get_customer(code)
        cust.name = name
        updated = await self._repo.update(cust)

        # update caches
        self._get_cache[code] = updated
        self._list_cache.clear()
        return updated
