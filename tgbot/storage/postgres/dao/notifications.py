from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.notification import Notification, StatusNotification


class NotificationDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_created_notifications(self):
        stmt = select(Notification).where(
            Notification.status == StatusNotification.CREATED,
            Notification.producer == "bot",
        )
        res = await self.session.execute(stmt)
        return res.scalars()

    async def update_notification_status(
        self, notification_id: int, status: StatusNotification
    ):
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=status)
        )
        await self.session.execute(stmt)
