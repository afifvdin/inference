from app.models.tagger import get_model, get_tokens_key_to_index


class State:
    def __init__(self):
        self.pos_tagger_model = get_model()
        self.pos_tagger_tokens_key_to_index = get_tokens_key_to_index()
