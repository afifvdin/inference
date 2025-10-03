from fastapi import APIRouter, Depends

from app.core.state import State
from app.models.tagger import model_predict
from app.schema import PosTaggerPredictBody, PosTaggerPredictResponse
from app.utils.get_state import get_state

pos_tagger_router = APIRouter(prefix="/pos-tagger", tags=["pos_tagger"])


@pos_tagger_router.post("/predict", response_model=PosTaggerPredictResponse)
def predict(body: PosTaggerPredictBody, state: State = Depends(get_state)) -> PosTaggerPredictResponse:
    result = model_predict(state.pos_tagger_model, state.pos_tagger_tokens_key_to_index, body.text)
    return PosTaggerPredictResponse(result=result)
