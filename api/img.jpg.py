from http.server import BaseHTTPRequestHandler
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


def make_image_from_text(text):
    font_size = 72
    font_filepath = "arial.ttf"
    arial = ImageFont.truetype(font_filepath, font_size)

    img = Image.new("RGB", (600, 200))
    drawable = ImageDraw.Draw(img)
    drawable.text((20, 20), text, font=arial, fill=(255, 255, 255))

    return img


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.headers.get("x-forwarded-for")
        image = make_image_from_text("Got your ip bro:\n" + ip)
        img_file = BytesIO()
        image.save(img_file, 'jpeg')

        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.send_header("Content-length", str(img_file.tell()))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        image.save(self.wfile, "JPEG")
