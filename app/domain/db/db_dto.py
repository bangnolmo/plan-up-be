from pydantic import BaseModel


class UpdateRequestDTO(BaseModel):
    auth: str
    year: int
    hakgi: int
    jojik: list = []
    classes: list = []
