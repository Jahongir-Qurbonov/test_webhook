from typing import TypedDict

from pydantic import BaseModel


# API request/response schemas
class StartRequest(BaseModel):
    msg: str


class StartResponse(BaseModel):
    part1: str | None


class FinishResponse(BaseModel):
    msg: str | None


class CallbackRequest(BaseModel):
    part2: str


class CallbackResponse(BaseModel):
    part2: str


# Internal data schemas
class InterviewResponse(TypedDict):
    part1: str


class InterviewFinalResponse(TypedDict):
    msg: str
