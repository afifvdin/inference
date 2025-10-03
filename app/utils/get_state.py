from typing import cast

from fastapi import Request

from app.core.state import State


def get_state(request: Request) -> State:
    return cast(State, request.app.state.state)
