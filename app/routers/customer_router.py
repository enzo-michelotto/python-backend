from xml.dom import NotFoundErr
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.customer_schemas import CustomerCreate, CustomerRead
from app.services.customer_service import CustomerService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/customers", tags=["customers"])


async def get_customer_service(
    db: AsyncSession = Depends(get_db),
) -> CustomerService:
    from app.repositories.sql_customer_repository import SqlCustomerRepository

    repo = SqlCustomerRepository(db)  # type: ignore
    return CustomerService(repo)


@router.post(
    "/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.create_customer(payload.code, payload.name)


@router.get("/{code}", response_model=CustomerRead)
async def read_customer(
    code: str,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.get_customer(code)


@router.put("/{code}", response_model=CustomerRead)
async def update_customer(
    code: str,
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        return await service.update_customer(code, payload.name)
    except NotFoundErr:
        raise HTTPException(404, "Customer not found")


@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    code: str,
    service: CustomerService = Depends(get_customer_service),
):
    try:
        await service.delete_customer(code)
    except NotFoundErr:
        raise HTTPException(404, "Customer not found")


@router.get("/", response_model=list[CustomerRead])
async def list_customers(
    service: CustomerService = Depends(get_customer_service),
):
    return await service.list_customers()
