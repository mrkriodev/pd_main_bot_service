import enum

from sqlalchemy import Integer, Enum, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class StatusNotification(enum.Enum):
    CREATED = "CREATED"
    DELIVERED = "DELIVERED"

    UNKNOWN = "UNKNOWN"

    ERROR = "ERROR"
    ERROR_USER_BLOCK = "ERROR_USER_BLOCK"


class Notification(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_uuid"), nullable=True)

    producer: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[StatusNotification] = mapped_column(
        Enum(StatusNotification, name="status_notification"),
        nullable=False,
        default=StatusNotification.CREATED,
        server_default="CREATED",
    )
