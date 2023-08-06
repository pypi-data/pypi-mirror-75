import argparse
import os

from PIL import Image
from PIL import ImageFont

from fluepdot import Fluepdot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default=os.getenv('FLIPDOT_URL'))
    subparsers = parser.add_subparsers(dest='method', required=True, help='method to execute')

    image_parser = subparsers.add_parser('image')
    image_parser.add_argument('path', help='path to image file')

    text_parser = subparsers.add_parser('text')
    text_parser.add_argument('message', help='text to send')
    text_parser.add_argument('--font', help='font to use')

    args = parser.parse_args()
    if args.url is None:
        parser.error('please specify a URL parameter or set the FLIPDOT_URL environment variable')

    fluepdot = Fluepdot(args.url)

    if args.method == 'image':
        image = Image.open(args.image)
        fluepdot.paste_image(image)
    elif args.method == 'text':
        font = ImageFont.truetype(args.font, fluepdot.height) if args.font else None
        fluepdot.render_text(args.message, font=font)

    fluepdot.update()

