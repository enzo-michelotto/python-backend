import os
import asyncio
import pytest
import pytest_asyncio
from xml.dom import NotFoundErr

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.repositories.sql_customer_repository import SqlCustomerRepository
from app.services.customer_service import CustomerService


@pytest.fixture(scope="session")
def db_url():
    return os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")


@pytest.fixture(scope="session")
def event_loop():
    """
    Create a session-scoped event loop for pytest-asyncio.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine(db_url):
    """
    Create an AsyncEngine and run Base.metadata.create_all once.
    """
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture  # type: ignore
def session_factory(engine):
    """
    Provide a sessionmaker for creating AsyncSession instances.
    """
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(session_factory):
    """
    Yield a fresh AsyncSession for each test, rolling back at teardown.
    """
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def repository(session):
    return SqlCustomerRepository(session)


@pytest.fixture
def service(repository):
    return CustomerService(repository)


@pytest.mark.asyncio
async def test_full_crud_flow(service: CustomerService, session: AsyncSession):
    created = await service.create_customer("C001", "Alice")
    assert created.code == "C001"  # type: ignore
    assert created.name == "Alice"  # type: ignore
    await session.commit()

    fetched = await service.get_customer("C001")
    assert fetched.id == created.id  # type: ignore
    assert fetched.name == "Alice"  # type: ignore

    all_customers = await service.list_customers()
    assert len(all_customers) == 1
    assert all_customers[0].code == "C001"  # type: ignore

    # UPDATE
    updated = await service.update_customer("C001", "Alice Smith")
    assert updated.name == "Alice Smith"  # pyright: ignore[reportGeneralTypeIssues]
    await session.commit()

    # VERIFY UPDATE
    reloaded = await service.get_customer("C001")
    assert reloaded.name == "Alice Smith"  # pyright: ignore[reportGeneralTypeIssues]

    # DELETE
    await service.delete_customer("C001")
    await session.commit()

    # VERIFY DELETION
    remaining = await service.list_customers()
    assert remaining == []


@pytest.mark.asyncio
async def test_not_found_errors(service: CustomerService):
    with pytest.raises(NotFoundErr):
        await service.get_customer("NOPE")

    with pytest.raises(NotFoundErr):
        await service.delete_customer("NOPE")
