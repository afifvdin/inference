from pydantic import BaseModel


class PosTaggerPredictResponse(BaseModel):
    result: list[tuple[str, str]]


class PosTaggerPredictBody(BaseModel):
    text: str
