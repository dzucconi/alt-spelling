#!/usr/bin/env python3

import argparse
import sys
import random
import time
import size
import size
import hue
import numpy as np
from PIL import Image
from progress.bar import ChargingBar
from glob import glob

Image.MAX_IMAGE_PIXELS = None

parser = argparse.ArgumentParser()

parser.add_argument('--width', help='Target width in inches',
                    default=30, type=float)
parser.add_argument('--height', help='Target height in inches',
                    default=36.667, type=float)
parser.add_argument(
    '--size', help='Size in pixels to slice tiles', default=13, type=int)
parser.add_argument('--dpi', help='Target dots per inch',
                    default=300, type=int)
parser.add_argument('--anchor', help='Crop anchor position', default='center')
parser.add_argument('--filename', help='Output filename',
                    default=f'output_{int(time.time())}')
parser.add_argument('--dir', help='Directory to process',
                    default='source/example/*.jpg')
parser.add_argument('--hue', help="Rotate hues",
                    default=False, type=bool)

args = parser.parse_args()

CONFIG = {
    'width': int(args.width * args.dpi),
    'height': int(args.height * args.dpi),
    'size': args.size,
    'anchor': args.anchor,
    'filename': args.filename,
    'images':  list(map(Image.open, glob(args.dir)))
}

np.random.shuffle(CONFIG.get('images'))

cropping_bar = ChargingBar('Cropping', max=len(CONFIG.get('images')))


def crop(img):
    cropping_bar.next()
    return size.crop(img, (CONFIG.get('width'), CONFIG.get('height')), anchor=CONFIG.get('anchor'))


CROPPED = list(map(crop, CONFIG.get('images')))

cropping_bar.finish()

x = CONFIG.get('width') // CONFIG.get('size')
y = CONFIG.get('height') // CONFIG.get('size')

print('Building map...')

mapping = [(
    xb * CONFIG.get('size'),
    yb * CONFIG.get('size'),
    (xb + 1) * CONFIG.get('size'),
    (yb + 1) * CONFIG.get('size'),
) for yb in range(y) for xb in range(x)]

coords = list(mapping)

print('Building output...')

output = Image.new('RGB', (CONFIG.get('width'), CONFIG.get('height')))

SET = CROPPED

rows = 0
offset = 0
processing_bar = ChargingBar('Processing', max=len(coords))

for i, box in enumerate(coords, start=1):
    processing_bar.next()

    which = (i + offset) % len(SET)

    if (args.hue):
        degree = 360 / ((i % (len(SET) - 1.0)) + 1.0)
        degree = 360 / (i % (len(SET)) + 1.0)
        degree = (90, 180, 270, 0)[i % 4]
        crop = SET[which].crop(box)
        colored = hue.colorize(crop, degree)

    crop = SET[which].crop(box)
    output.paste(crop, box)

processing_bar.finish()

print('Saving...')

output.save(f'processed/{CONFIG.get("filename")}.png', 'PNG', quality=100)

print('Done.')
