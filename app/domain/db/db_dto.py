from pydantic import BaseModel


class CrawlRequestDTO(BaseModel):
    auth: str
    year: int
    hakgi: int
    jojik: list = []
    classes: list = []
