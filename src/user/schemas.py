from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserIn(UserBase):
    pass


class UserOut(UserBase):
    id: int
