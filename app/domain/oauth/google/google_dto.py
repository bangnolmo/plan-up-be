from pydantic import BaseModel


class RefreshUserDTO(BaseModel):
    refresh: str
    email: str