from aiogram_dialog.widgets.text import Jinja

WELCOM_MESSAGE_RU = Jinja("""
🚀 PumpDump — это инновационные приложение, которое позволяет делать ставки на криптовалюты.

Присоединяйтесь к нашему сообществу и следите за всеми новостями и обновлениями в <a href="https://t.me/pumpdump_app_official"> официальном канале.</a>
""")


TEXT_TECHNICAL_SUPPORT_RU = Jinja("""
Если у Вас случилась какая-то проблема. Опишите ее.
""")

TEXT_PROFILE_RU = Jinja("""
Поделись своей реферальной ссылкой и получи бонус:

<code>{{link}}</code>

Количество приглашений: {{count_reff}}

Информация о вашем кошельке:

{% if address %}
    <code>{{address}}</code>
{% else %}
    <b>Вы не подключили еще кошелек.</b>
{% endif %}
""")

TEXT_BACK_RU = "Назад"
TEXT_WHEN_USER_SEND_PROBLEM_RU = "Ваш вопрос передан в техническую поддержку. Спасибо за обращение."