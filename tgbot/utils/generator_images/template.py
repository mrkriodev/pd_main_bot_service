import os


class TemplateOrderSharedLink:
    CONTAINER_GREEN_BACKGROUND_COLOR = "0 0 30px rgba(0, 255, 0, 0.5);"
    CONTAINER_RED_BACKGROUND_COLOR = "0 0 30px rgba(255, 0, 0, 0.5);"
    PROGRESS_BAR_GREEN_BACKGROUND_COLOR = "2px 2px 10px rgba(0, 255, 0, 0.8);"
    PROGRESS_BAR_RED_BACKGROUND_COLOR = "2px 2px 10px rgba(255, 0, 0, 0.8);"
    GREEN = "#00ff00"
    RED = "#ff4444"


class TemplateHTML(TemplateOrderSharedLink):
    TEMPLATE_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "template"
    )
    OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

    SRC_BASE = "data:image/jpeg;base64,"

    def __init__(self):
        self.SHARED_ORDER_USER_HTML = self.load_file(
            os.path.join(self.TEMPLATE_FOLDER, "shared_order.html")
        )
        self.PIC_SHARED_ORDER_USER = self.SRC_BASE + self.load_file(
            os.path.join(self.TEMPLATE_FOLDER, "shared_order_img_base64")
        )

    @staticmethod
    def load_file(file_path: str) -> str:
        with open(file_path, "r") as image_base64_file:
            return image_base64_file.read()
