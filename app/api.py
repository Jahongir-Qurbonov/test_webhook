from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import session as db_session
from .repository import get_or_create_code
from .schemas import (
    CallbackRequest,
    CallbackResponse,
    FinishResponse,
    StartRequest,
    StartResponse,
)
from .services import fetch_final_message, save_second_part, send_initial_request

router = APIRouter()


@router.post("/start", response_model=StartResponse)
async def start(
    data: StartRequest,
    session: AsyncSession = Depends(db_session),
):
    part1 = await send_initial_request(session, data.msg)
    print("Initial part sent, received part1:", part1)

    return StartResponse(part1=part1)


@router.post("/callback", response_model=CallbackResponse)
async def callback(
    data: CallbackRequest,
    session: AsyncSession = Depends(db_session),
):
    print("Callback received body:", data)
    part2 = data.part2

    await save_second_part(session, part2)

    return CallbackResponse(part2=part2)


@router.get("/finish", response_model=FinishResponse)
async def finish_interview(
    session: AsyncSession = Depends(db_session),
):
    code = await get_or_create_code(session)
    msg = await fetch_final_message(session, code)

    return FinishResponse(msg=msg)
