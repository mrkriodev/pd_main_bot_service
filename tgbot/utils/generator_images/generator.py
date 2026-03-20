import logging
import uuid
from decimal import Decimal
from urllib.parse import quote_plus

import aiofiles
import aiohttp

from config import settings
from utils.generator_images.template import TemplateHTML


class GeneratorHTML(TemplateHTML):

    def generate_html_shared_result_order(
        self,
        pair: str,
        result: Decimal | float,
        profit: bool,
        open_order: Decimal | float,
        close_close: Decimal | float,
    ):

        if profit:
            color = self.GREEN
            result = f"+ {result}%"
            container_shadow = self.CONTAINER_GREEN_BACKGROUND_COLOR
            profit_shadow = self.PROGRESS_BAR_GREEN_BACKGROUND_COLOR

        else:
            color = self.RED
            result = f"- {result}%"
            container_shadow = self.CONTAINER_RED_BACKGROUND_COLOR
            profit_shadow = self.PROGRESS_BAR_RED_BACKGROUND_COLOR

        html = self.SHARED_ORDER_USER_HTML
        html = html.replace("|thisSrc|", self.PIC_SHARED_ORDER_USER)
        html = html.replace("|thisPair|", pair)
        html = html.replace("|thisResult|", result)
        html = html.replace("|thisColor|", color)
        # html = html.replace("|thisWorth|", worth)
        html = html.replace("|thisInitial|", str(open_order))
        html = html.replace("|thisCurrent|", str(close_close))
        html = html.replace("|thisContainerShadow|", container_shadow)
        html = html.replace("|thisProfitShadow|", profit_shadow)
        return html

    async def save_html(self, data: str):
        random_filename = quote_plus(uuid.uuid4().hex) + ".html"
        path_to_file = self.OUTPUT_FOLDER + "/" + random_filename
        print(f"path_to_file: {path_to_file}")
        async with aiofiles.open(path_to_file, mode="w") as file:
            await file.write(data)
        return random_filename

    @staticmethod
    async def get_image(image_url: str):
        params = [
            ("u", settings.bot.notification.username_service_convert),
            ("p", settings.bot.notification.password_service_convert),
            ("url", image_url),
            ("format", "jpeg"),
        ]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"{settings.bot.notification.url_service_convert}/convert/html2image",
                params=params,
            ) as r:
                if r.status == 200:
                    return await r.read()
                else:
                    response = await r.text()
                    logging.error(f"Error convert html to image: {response}")
                    return None
