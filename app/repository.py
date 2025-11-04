from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Code


async def get_or_create_code(session: AsyncSession) -> Code:
    async with session as _session:
        result = await _session.execute(select(Code).limit(1))
        code_part = result.scalar_one_or_none()

        if code_part is None:
            code_part = Code()
            _session.add(code_part)
            await _session.commit()
            await _session.refresh(code_part)

        return code_part


async def store_code(session: AsyncSession, instance: Code) -> Code:
    async with session as _session:
        _session.add(instance)
        await _session.commit()
        await _session.refresh(instance)

        return instance
