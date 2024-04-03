from http.server import BaseHTTPRequestHandler
from PIL import Image, ImageFont


def make_image_from_text(text):
    font_size = 72
    font_filepath = "arial.ttf"
    color = (255, 255, 255)

    font = ImageFont.truetype(font_filepath, size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGB", mask_image.size)
    img.im.paste(
        color,
        (0, 0) + mask_image.size,
        mask_image
    )  # need to use the inner `img.im.paste` due to `getmask` returning a core
    return img


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()

        ip = self.headers.get("x-forwarded-for")
        image = make_image_from_text("Got your ip bro: " + ip)

        image.save(self.wfile, "JPEG")
