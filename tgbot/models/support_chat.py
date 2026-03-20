from sqlalchemy import BigInteger, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SupportChat(Base):
    __tablename__ = "support_chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=True)
