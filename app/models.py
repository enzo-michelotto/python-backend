from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerEntity(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name
