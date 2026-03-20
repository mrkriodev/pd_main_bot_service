from aiogram_dialog.widgets.input import MessageInput


def kbn_technical_support(on_click):
    return MessageInput(
        func=on_click,
        content_types=["text"],
    )
