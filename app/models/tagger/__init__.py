import json
import os
import sys
from typing import cast

import numpy as np
from gensim.models import Word2Vec
from keras.models import Model, load_model
from keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import TweetTokenizer
from numpy.typing import NDArray

__all__ = ["get_model", "get_tokens_key_to_index", "model_predict"]
_base_dir = os.path.dirname(os.path.abspath(__file__))
if _base_dir not in sys.path:
    sys.path.append(_base_dir)

with open(os.path.join(_base_dir, "slang.json"), "r", encoding="utf-8") as f:
    _slang: dict[str, str] = json.load(f)

_tags = [
    "CC",
    "CD",
    "OD",
    "DT",
    "FW",
    "IN",
    "JJ",
    "MD",
    "NEG",
    "NN",
    "NNP",
    "NND",
    "PR",
    "PRP",
    "RB",
    "RP",
    "SC",
    "SYM",
    "UH",
    "VB",
    "WH",
    "Z",
    "AT",
    "HASH",
    "URL",
    "EMO",
    "<PAD>",
]


def _normalize(tokens: list[str]) -> list[str]:
    res = tokens.copy()
    for index, token in enumerate(res):
        if token in _slang:
            res[index] = _slang[token]
    return res


def get_model() -> Model:
    return cast(Model, load_model(os.path.join(_base_dir, "model.keras")))


def get_tokens_key_to_index() -> dict[str, int]:
    wv = Word2Vec.load(os.path.join(_base_dir, "wv.model"))
    return cast(dict[str, int], wv.wv.key_to_index)


def model_predict(model: Model, tokens_key_to_index: dict[str, int], sentence: str) -> list[tuple[str, str]]:
    tokens: list[str] = TweetTokenizer().tokenize(sentence)
    tokens = _normalize(tokens)

    tokens_id: list[int] = []
    for token in tokens:
        if token in tokens_key_to_index:
            tokens_id.append(tokens_key_to_index[token])
        else:
            tokens_id.append(tokens_key_to_index["<UNK>"])

    tokens_padded: NDArray[np.int32] = pad_sequences(
        [tokens_id],
        padding="post",
        maxlen=74,
        value=tokens_key_to_index["<PAD>"],
    )[0]

    result: NDArray[np.float32] = model.predict(np.array([tokens_padded]))

    tags = [_tags[np.argmax(i)] for i in result[0]]
    pairs: list[tuple[str, str]] = []
    for word, tag in zip(tokens, tags):
        if tag == "<PAD>" and word == "<PAD>":
            continue
        pairs.append((word, tag))

    return pairs
