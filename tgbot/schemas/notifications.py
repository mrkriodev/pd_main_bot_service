from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, model_validator


class TypeNotificationEnum(str, Enum):
    order = "order"
    shared_link = "shared_link"
    broadcast_message = "broadcast_message"


class TypeNotificationSchema(BaseModel):
    type: Optional[TypeNotificationEnum] = None

    @model_validator(mode="before")
    def check_type(cls, values):
        notification_type = values.get("type")
        if (
            notification_type
            and notification_type not in TypeNotificationEnum.__members__.values()
        ):
            values["type"] = None
        return values


class OrderNotificationSchema(BaseModel):
    type: str
    order_id: int
    status: str


class SharedLinkNotificationSchema(BaseModel):
    type: str
    pair: str
    result: Decimal | float
    profit: bool
    open_order: Decimal | float
    close_order: Decimal | float


class BroadCastNotificationSchema(BaseModel):
    pass
