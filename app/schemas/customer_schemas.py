from pydantic import BaseModel, Field, model_validator


class CustomerCreate(BaseModel):
    code: str = Field(..., pattern=r"^CUST\d{7}$")
    name: str

    @model_validator(mode="before")
    def uppercase_code(cls, values):
        values["code"] = values["code"].upper()
        return values


class CustomerRead(BaseModel):
    id: int
    code: str
    name: str

    model_config = {"from_attributes": True}
