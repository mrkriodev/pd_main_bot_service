import asyncio
import logging

from aiogram.types import Message, BufferedInputFile
#from dexlotdb.models.order import StatusOrder
from models.pduser import PDUser
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserMessageSchema, SupportMessageSchema
#from storage.postgres.dao.orders import OrderDao
from storage.postgres.dao.orders import BetDAO
from storage.postgres.dao.users import UserDAO
from utils.render_img.draw import work_image
from utils.shared import get_message_for_shared_order


class UsersService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_dao = UserDAO(session=session)
        self.order_dao = BetDAO(session=session)

    async def get_user(self, user_id: int) -> PDUser:
        return await self.user_dao.get_user(user_id)

    async def count_reff_users_by_user_id(self, user_id) -> int:
        count = await self.user_dao.count_reff_users_by_user(user_id=user_id)
        return count if count else 0

    async def add_new_user(self, user_data: UserMessageSchema):
        if await self.user_dao.get_user(user_id=user_data.id):
            return
        await self.user_dao.create_user(user=user_data)
        await self.session.commit()

    async def add_new_user_from_reff_user(self, user_data: UserMessageSchema):
        user = await self.user_dao.get_user(user_id=user_data.id)
        if user is not None:
            return
        reff_user = await self.user_dao.get_user(user_id=user_data.reff_user_id)
        if reff_user is None:
            user_data.reff_user_id = None
            await self.user_dao.create_user(user=user_data)
            await self.session.commit()
        else:
            await self.user_dao.create_user(user=user_data)
            await self.session.commit()

    async def receive_message_from_user_help(self, message: Message):
        user = await self.user_dao.get_user(user_id=message.from_user.id)
        if user is None:
            user_data = UserMessageSchema(**(message.from_user.model_dump()))
            await self.user_dao.create_user(user=user_data)

        mess = SupportMessageSchema(
            user_id=message.from_user.id,
            message_id=message.message_id or 0,
            message=message.text or "",
        )
        await self.user_dao.add_support_message(mess)
        await self.session.commit()

    async def create_shared_order(self, message: Message, user_id: int, order_id: int):
        bet = await self.order_dao.get_order_of_user(order_id=order_id, user_id=user_id)
        if bet is None:
            logging.warning(f"User: {user_id} shared not exist bet: {order_id}")
            return None

        if bet.close_price is None:
            logging.warning(f"User: {user_id} shared not closed bet: {order_id}")
            return None

        result_profit = (
            (bet.close_price / bet.open_price) * 100 - 100
            if bet.open_price != 0
            else 0
        )
        pair_parts = [p.strip() for p in bet.pair.replace("-", "/").split("/")]
        base_symbol = pair_parts[0] if len(pair_parts) > 0 else ""
        quote_symbol = pair_parts[1] if len(pair_parts) > 1 else ""

        image_bytes = await asyncio.to_thread(
            work_image.get_image_for_share_order,
            base_symbol,
            quote_symbol,
            True if result_profit >= 0 else False,
            result_profit,
            bet.open_price,
            bet.close_price,
        )

        caption = get_message_for_shared_order(user_id=message.from_user.id)

        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=BufferedInputFile(file=image_bytes, filename="image.png"),
            caption=caption,
        )
