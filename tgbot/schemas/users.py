from pydantic import BaseModel, Field
from uuid import UUID


class UserMessageSchema(BaseModel):
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str | None
    inviter_deeplink_refcode: str | None = None


class SupportMessageSchema(BaseModel):
    user_id: int
    message_id: int
    message: str


class PDUserScheme(BaseModel):
    id: int | None = None
    user_uuid: UUID | None = None
    referrer_user_uuid: UUID | None = None
    main_ref: str | None = None
    add_refs: list[str] = Field(default_factory=list)
    authorized_fully: bool = False
    session_id: str | None = None
    google_id: str | None = None
    google_email: str | None = None
    google_name: str | None = None
    telegram_id: int | None = None
    telegram_username: str | None = None
    telegram_first_name: str | None = None
    telegram_last_name: str | None = None
    auth_provider: str | None = None
    created_at: int | None = None
    updated_at: int | None = None
    last_login_at: int | None = None
