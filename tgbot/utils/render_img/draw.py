import os
from decimal import Decimal
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager


class LocalImage:
    def __init__(self):
        self.img = self.get_img()

    @staticmethod
    def get_img():
        with Image.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "macro.jpeg")
        ) as img:
            copy_img = img.copy()
        return copy_img

    def get_image_for_share_order(
        self,
        base_token: str,
        quote_token: str,
        sign_of_order: bool,
        bet_sum: Decimal, #percent: Decimal,
        open_price: Decimal,
        close_price: Decimal,
    ):
        copy_img = self.img.copy()
        draw = ImageDraw.Draw(copy_img)
        reg_font_path = font_manager.FontProperties(
            family="sans-serif", weight="normal"
        )
        bold_font_path = font_manager.FontProperties(family="sans-serif", weight="bold")
        reg_font = font_manager.findfont(reg_font_path)
        bold_font = font_manager.findfont(bold_font_path)
        # Upscaled for readability on mobile / bot previews
        font_small = ImageFont.truetype(reg_font, 26)
        font_medium = ImageFont.truetype(bold_font, 40)
        font_large = ImageFont.truetype(bold_font, 68)
        # Larger than font_small for Initial / Current worth lines
        font_worth = ImageFont.truetype(bold_font, 36)

        # Horizontal indent: 3× previous left margin (was 42 → 126)
        x = 42 * 3
        positions = [(x, 88), (x, 188), (x, 308), (x, 358)]

        # Рисуем первую строку
        draw.text(
            positions[0],
            f"{base_token}/{quote_token}",
            fill=(75, 199, 249),
            font=font_medium,
        )
        bbox = draw.textbbox(
            positions[0], f"{base_token}/{quote_token}", font=font_medium
        )
        width = bbox[2] - bbox[0]
        draw.text(
            (positions[0][0] + width, positions[0][1]),
            " | PUMPDUMP",
            fill=(175, 175, 175),
            font=font_medium,
        )

        # Рисуем вторую строку
        sign = "+" if sign_of_order else ""
        fill = (0, 255, 0, 255) if sign_of_order else (255, 0, 0, 255)
        draw.text(
            positions[1],
            f"{sign}{abs(bet_sum)}", #f"{sign}{percent.quantize(Decimal('0.00'))}%",
            fill=fill,
            font=font_large,
        )

        # Рисуем третью строку
        draw.text(
            positions[2], "Initial price: ", fill=(255, 255, 255, 255), font=font_worth
        )
        bbox = draw.textbbox(positions[2], "Initial price: ", font=font_worth)
        width = bbox[2] - bbox[0]
        draw.text(
            (positions[2][0] + width, positions[2][1]),
            str(open_price.quantize(Decimal('0.00'))),
            fill=(75, 199, 249),
            font=font_worth,
        )

        # Рисуем четвертую строку
        draw.text(
            positions[3], "Last price: ", fill=(255, 255, 255, 255), font=font_worth
        )
        bbox = draw.textbbox(positions[3], "Last price: ", font=font_worth)
        width = bbox[2] - bbox[0]
        draw.text(
            (positions[3][0] + width, positions[3][1]),
            str(close_price.quantize(Decimal('0.00'))),
            fill=(75, 199, 249),
            font=font_worth,
        )
        # self.img.save("output_image.jpeg")
        byte_io = BytesIO()
        copy_img.save(byte_io, format="JPEG")
        byte_io.seek(0)  # Возвращаемся в начало потока
        return byte_io.getvalue()


work_image = LocalImage()
