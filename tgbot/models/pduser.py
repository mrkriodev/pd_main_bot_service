from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

# class Base(DeclarativeBase):
#     pass

from .base import Base


class PDUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )
    referrer_user_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    main_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    add_refs: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::TEXT[]")
    )
    authorized_fully: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    session_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    google_email: Mapped[str | None] = mapped_column(String(255))
    google_name: Mapped[str | None] = mapped_column(String(255))
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255))
    telegram_first_name: Mapped[str | None] = mapped_column(String(255))
    telegram_last_name: Mapped[str | None] = mapped_column(String(255))
    auth_provider: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )
    updated_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )
    last_login_at: Mapped[int | None] = mapped_column(BigInteger)
