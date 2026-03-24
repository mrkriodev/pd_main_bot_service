import logging
from typing import Any

import aiohttp
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from exceptions.main_backend import (
    MainBackendConfigError,
    MainBackendHttpSessionError,
    MainBackendRegistrationError,
)
from models.pduser import PDUser
from models.support_chat import SupportChat
from schemas.users import SupportMessageSchema, UserMessageSchema

logger = logging.getLogger(__name__)


class UserDAO:
    def __init__(
        self,
        session: AsyncSession,
        http_session: aiohttp.ClientSession | None = None,
    ):
        self.session = session
        self._http_session = http_session

    async def _register_user_via_backend(
        self,
        user: UserMessageSchema,
        referrer_code: str | None,
    ) -> None:
        if not settings.main_backend.admin_token.strip():
            raise MainBackendConfigError(
                "APP_CONFIG__MAIN_BACKEND__ADMIN_TOKEN is missing or empty"
            )
        if self._http_session is None:
            raise MainBackendHttpSessionError(
                "aiohttp ClientSession was not injected into UserDAO"
            )
        if self._http_session.closed:
            raise MainBackendHttpSessionError("aiohttp ClientSession is closed")

        base = settings.main_backend.base_url.rstrip("/")
        path = settings.main_backend.admin_register_path
        if not path.startswith("/"):
            path = "/" + path
        url = f"{base}{path}"

        body: dict[str, Any] = {
            "tg_id": user.id,
            "language": (user.language_code or "en")[:16],
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username or "",
        }
        if referrer_code:
            body["referrer"] = referrer_code

        headers = {
            "Content-Type": "application/json",
            "X-ADMIN-TOKEN": settings.main_backend.admin_token,
        }

        try:
            async with self._http_session.post(
                url,
                json=body,
                headers=headers,
            ) as resp:
                text = await resp.text()
                if resp.status < 200 or resp.status >= 300:
                    logger.warning(
                        "register_user HTTP %s body=%s",
                        resp.status,
                        text[:500],
                    )
                    raise MainBackendRegistrationError(
                        f"register_user failed with HTTP {resp.status}",
                        status=resp.status,
                        body=text[:4000],
                    )
        except aiohttp.ClientError as e:
            raise MainBackendRegistrationError(
                f"register_user request failed: {e}",
            ) from e

    async def create_user(self, user: UserMessageSchema) -> None:
        referrer_code: str | None = None
        if user.reff_user_id is not None:
            referrer = await self.get_user(user_id=user.reff_user_id)
            if referrer is not None and referrer.main_ref:
                referrer_code = referrer.main_ref

        await self._register_user_via_backend(user, referrer_code=referrer_code)

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
