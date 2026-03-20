from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class PDBetSchema(BaseModel):
    id: int | None = None
    user_uuid: UUID
    side: Literal["pump", "dump"]
    sum: Decimal
    pair: str
    timeframe: int
    open_price: Decimal
    close_price: Decimal | None = None
    open_time: datetime
    close_time: datetime | None = None
    created_at: int | None = None
    updated_at: int | None = None
