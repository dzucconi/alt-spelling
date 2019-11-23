#!/usr/bin/env python3

import sys
import random
import time
import size
import hue
import numpy as np
from PIL import Image
from progress.bar import ChargingBar
from glob import glob

CONFIG = {
    'width': 9000,  # 30
    'height': 11000,  # 36.667
    'size': 15,
    'anchor': 'center',
    'filename': f'output_{int(time.time())}',
    'images':  list(map(Image.open, glob('source/x/*.jpg'))) +
    [
        Image.open('source/x.jpg'),
    ],
}

np.random.shuffle(CONFIG.get('images'))

cropping_bar = ChargingBar('Cropping', max=len(CONFIG.get('images')))


def cropit(img):
    cropping_bar.next()
    return size.crop(img, (CONFIG.get('width'), CONFIG.get('height')), anchor=CONFIG.get('anchor'))


CROPPED = list(map(cropit, CONFIG.get('images')))

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

    # new_row = box[0] == 0
    # if new_row:
    #     # offset = (rows % (len(SET) // 2))
    #     offset = rows % len(SET)
    #     rows = rows + 1

    which = (i + offset) % len(SET)

    # degree =  360 / ((i % (len(SET) - 1.0)) + 1.0)
    # degree =  360 / (i % (len(SET)) + 1.0)
    # degree = (90, 180, 270, 0)[i % 4]
    # crop = SET[which].crop(box)
    # colored = hue.colorize(crop, degree)

    crop = SET[which].crop(box)
    output.paste(crop, box)

processing_bar.finish()

print('Saving...')
output.save(f'processed/{CONFIG.get("filename")}.png', 'PNG', quality=100)
print('Done.')
