from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    email: EmailStr
    name: str
    password: str

    model_config = ConfigDict(from_attributes=True)