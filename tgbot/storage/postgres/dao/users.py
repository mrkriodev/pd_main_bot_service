from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.pduser import PDUser
from schemas.users import UserMessageSchema
#from dexlotdb.models import SupportChat
from models.support_chat import SupportChat
from schemas.users import SupportMessageSchema


class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserMessageSchema):
        referrer_uuid = None
        if user.reff_user_id is not None:
            referrer = await self.get_user(user_id=user.reff_user_id)
            if referrer is not None:
                referrer_uuid = referrer.user_uuid

        pd_user = PDUser(
            telegram_id=user.id,
            telegram_username=user.username,
            telegram_first_name=user.first_name,
            telegram_last_name=user.last_name,
            auth_provider="telegram",
            referrer_user_uuid=referrer_uuid,
        )
        self.session.add(pd_user)
        await self.session.flush()

    async def get_user(self, user_id: int) -> PDUser | None:
        stmt = select(PDUser).where(PDUser.telegram_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def add_support_message(self, message: SupportMessageSchema):
        mess = SupportChat(**(message.model_dump()))
        self.session.add(mess)

    async def count_reff_users_by_user(self, user_id):
        user = await self.get_user(user_id=user_id)
        if user is None or user.user_uuid is None:
            return 0
        stmt = (
            select(func.count())
            .select_from(PDUser)
            .where(PDUser.referrer_user_uuid == user.user_uuid)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

