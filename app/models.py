from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Code(Base):
    __tablename__ = "code_parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    req_msg: Mapped[str | None]
    part1: Mapped[str | None]
    part2: Mapped[str | None]
    final_code: Mapped[str | None]
    message: Mapped[str | None]
