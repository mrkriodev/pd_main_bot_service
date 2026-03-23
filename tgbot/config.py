from typing import Optional

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str   
    port: int
    user: str
    password: str
    name: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class WebHookSettings(BaseModel):
    web_server_host: str = "127.0.0.1"
    web_server_port: int = 8080

    webhook_path: str = "/webhook"
    webhook_secret: str = "my-secret"
    base_webhook_url: str = "https://example.com/"


class BotNotification(BaseModel):
    username_bot: str = "https://t.me/pumpdump_app_bot"
    username_channel: str = "https://t.me/pumpdump_app_official"
    link_to_nft_market: str = "https://getgems.io/dexlot"
    link_to_img: str = "https://pumpdumpapp.com/html"

    url_service_convert: str = ""
    username_service_convert: str = ""
    password_service_convert: str = ""


class BotSettings(BaseModel):
    token: str
    support_chat_id: int = -1003789795601  # pumpdump_channel
    #support_thread_id: int = 2
    run_polling: bool | None
    run_webhook: WebHookSettings | None
    webapp: Optional[str] = "https://pumpdumpapp.com/"
    notification: BotNotification = Field(default_factory=BotNotification)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    db: DatabaseSettings
    bot: BotSettings
    redis: RedisDsn | None = None
    rabbitmq: AmqpDsn | None = None


settings = Settings()
