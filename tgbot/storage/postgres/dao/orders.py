from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bet import Bet
from models.pduser import PDUser


class BetDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_of_user(
        self, order_id: int, user_id: int
    ) -> Bet | None:
        stmt = (
            select(Bet)
            .join(PDUser, Bet.user_uuid == PDUser.user_uuid)
            .where(
                Bet.id == order_id,
                PDUser.telegram_id == user_id,
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
