from __future__ import annotations

from decimal import Decimal

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

from .base import Base


class Bet(Base):
    __tablename__ = "bets"
    __table_args__ = (CheckConstraint("side IN ('pump','dump')", name="chk_bets_side"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    sum: Mapped[Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    pair: Mapped[str] = mapped_column(String(20), nullable=False)
    timeframe: Mapped[int] = mapped_column(Integer, nullable=False)
    open_price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    close_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 8))
    open_time: Mapped[object] = mapped_column(DateTime, nullable=False)
    close_time: Mapped[object | None] = mapped_column(DateTime)
    created_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )
    updated_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )
