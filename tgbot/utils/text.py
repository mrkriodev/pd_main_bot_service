from __future__ import annotations

from jinja2 import Template

OFFICIAL_CHANNEL_URL = "https://t.me/pumpdump_app_official"


def normalize_locale(language_code: str | None) -> str:
    """Telegram language_code; default English unless primary tag is Russian."""
    if not language_code:
        return "en"
    primary = language_code.lower().split("-", 1)[0]
    return "ru" if primary == "ru" else "en"


_WELCOME = {
    "en": Template(
        """
🚀 PumpDump is an innovative app for placing bets on cryptocurrencies.

Join our community and follow all news and updates on our <a href="{{ channel }}">official channel.</a>
""".strip()
    ),
    "ru": Template(
        """
🚀 PumpDump — это инновационные приложение, которое позволяет делать ставки на криптовалюты.

Присоединяйтесь к нашему сообществу и следите за всеми новостями и обновлениями в <a href="{{ channel }}"> официальном канале.</a>
""".strip()
    ),
}

_TECH_SUPPORT = {
    "en": Template("If something went wrong, please describe the issue."),
    "ru": Template("Если у Вас случилась какая-то проблема. Опишите ее."),
}

# <code>{{ link }}</code>

_PROFILE = {
    "en": Template(
        """
Share your referral link and get a bonus:

<a href="{{ link }}">{{ link }}</a>

Invites: {{ count_reff }}

Your wallet:

{% if address %}
    <code>{{ address }}</code>
{% else %}
    <b>You have not connected a wallet yet.</b>
{% endif %}
""".strip()
    ),
    "ru": Template(
        """
Поделись своей реферальной ссылкой и получи бонус:

<a href="{{ link }}">{{ link }}</a>

Количество приглашений: {{ count_reff }}

Информация о вашем кошельке:

{% if address %}
    <code>{{ address }}</code>
{% else %}
    <b>Вы не подключили еще кошелек.</b>
{% endif %}
""".strip()
    ),
}

_BACK = {"en": "Back", "ru": "Назад"}

_SUPPORT_ACK = {
    "en": "Your message has been sent to support. Thank you for reaching out.",
    "ru": "Ваш вопрос передан в техническую поддержку. Спасибо за обращение.",
}


def render_welcome(language_code: str | None) -> str:
    loc = normalize_locale(language_code)
    return _WELCOME[loc].render(channel=OFFICIAL_CHANNEL_URL)


def render_technical_support_prompt(language_code: str | None) -> str:
    loc = normalize_locale(language_code)
    return _TECH_SUPPORT[loc].render()


def render_profile(
    language_code: str | None,
    *,
    link: str,
    count_reff: int,
    address: str | None = None,
) -> str:
    loc = normalize_locale(language_code)
    return _PROFILE[loc].render(
        link=link, count_reff=count_reff, address=address
    )


def back_button_label(language_code: str | None) -> str:
    return _BACK[normalize_locale(language_code)]


def support_message_ack(language_code: str | None) -> str:
    return _SUPPORT_ACK[normalize_locale(language_code)]
