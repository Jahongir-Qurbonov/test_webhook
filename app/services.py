import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from yarl import URL

from .config import settings
from .cookiejar import load_cookies_from_file, save_cookies_to_file
from .models import Code
from .repository import get_or_create_code, store_code
from .schemas import InterviewFinalResponse, InterviewResponse

API_URL = "https://test.icorp.uz/interview.php"
CALLBACK_URL = URL(settings.CALLBACK_URL)


async def send_initial_request(session: AsyncSession, msg: str) -> str | None:
    code = await get_or_create_code(session)
    code.req_msg = msg
    code.part1 = None
    code = await store_code(session, code)

    callback_url = str(CALLBACK_URL.with_path("/callback"))

    cookiejar = load_cookies_from_file()
    async with aiohttp.ClientSession(cookie_jar=cookiejar) as client:
        async with client.post(
            API_URL,
            json={"msg": msg, "url": callback_url},
        ) as resp:
            try:
                resp_data: InterviewResponse = await resp.json()
            except aiohttp.ContentTypeError:
                print("Error parsing JSON:", await resp.text())
                return None

            code.part1 = resp_data["part1"]
            code = await store_code(session, code)
            assert code.part1 is not None

            save_cookies_to_file(cookiejar)

            return code.part1


async def save_second_part(session: AsyncSession, part2: str):
    code = await get_or_create_code(session)

    code.part2 = part2
    code = await store_code(session, code)


async def fetch_final_message(session: AsyncSession, code: Code) -> str | None:
    if code.part1 is None or code.part2 is None:
        return None

    final_code = f"{code.part1}{code.part2}"

    cookiejar = load_cookies_from_file()
    async with aiohttp.ClientSession(cookie_jar=cookiejar) as client:
        async with client.get(API_URL, params={"code": final_code}) as resp:
            try:
                resp_data: InterviewFinalResponse = await resp.json()
            except aiohttp.ContentTypeError:
                code.message = None
                await store_code(session, code)
                print("Error parsing JSON:", await resp.text())
                return None

            code.message = resp_data["msg"]
            code = await store_code(session, code)

            save_cookies_to_file(cookiejar)

            return code.message
