import socket

import requests

from PIL import Image, ImageDraw


class Fluepdot:
    class RenderingMode:
        FULL = 0
        DIFFERENTIAL = 1

    def __init__(self, hostname: str, rendering_mode=RenderingMode.FULL):
        host = socket.gethostbyname(hostname)
        self.base_url = 'http://' + host
        self.image = self.load_framebuffer()
        self.width, self.height = self.image.size
        if rendering_mode != Fluepdot.RenderingMode.FULL:
            self.set_rendering_mode(rendering_mode)

    @property
    def dimensions(self):
        return self.width, self.height

    def load_framebuffer(self) -> Image:
        res = requests.get(self.base_url + '/framebuffer')
        rows = res.text.splitlines()
        width = len(rows[0])
        height = len(rows)
        image = Image.new(size=(width, height), mode='1')
        for row_index, row in enumerate(rows):
            for column_index, pixel in enumerate(row):
                if pixel == 'X':
                    image.putpixel((column_index, row_index), 1)
        return image

    # not working yet (connection abort)
    def set_rendering_timings(self, pre_delay=0, clear_delay=160, set_delay=None, adjustments=None):
        set_delay = set_delay or clear_delay
        payload = ''
        for column_index in range(self.width):
            payload += f'{pre_delay:05d}\n{clear_delay:05d}\n{set_delay:05d}\n'
        print(payload)
        res = requests.post(self.base_url + '/rendering/timings', data=payload.encode('ascii'))
        if not res.ok:
            raise Exception(res.text)

    def set_rendering_mode(self, mode=RenderingMode.DIFFERENTIAL):
        res = requests.request('PUT', self.base_url + '/rendering/mode', data=str(mode))
        if not res.ok:
            raise Exception(res.text)

    def clear(self, invert=False):
        self.image = Image.new(mode='1', size=self.dimensions, color=1 if invert else 0)

    @staticmethod
    def encode_image(image: Image):
        width, height = image.size
        payload = ''
        for y in range(height):
            for x in range(width):
                payload += 'X' if image.getpixel((x, y)) else ' '
            payload += '\n'
        return payload

    def update(self):
        encoded = self.encode_image(self.image)
        res = requests.post(self.base_url + '/framebuffer', data=encoded)
        assert res.ok, res.text

    def render_text(self, text, font=None, x=0, y=0, *args, **kwargs):
        d = ImageDraw.Draw(self.image)
        d.multiline_text((x, y), text, font=font, fill=1, *args, **kwargs)

    def paste_image(self, image, box=None, mask=None):
        self.image.paste(image, box, mask)
