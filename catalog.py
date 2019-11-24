from PIL import Image
import glob
from progress.bar import ChargingBar

Image.MAX_IMAGE_PIXELS = None

filenames = glob.glob('./selects/*.png')

size = 2000, 2000

progress = ChargingBar('Processing', max=len(filenames))


def format(path):
    progress.next()
    img = Image.open(path)
    width, height = img.size

    print_width = f'{round(width / 300, 2)}in'
    print_height = f'{round(height / 300, 2)}in'

    filename = path.split('/')[-1]
    new_filename = f'./catalog/{print_width}x{print_height}__{filename}'
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(new_filename, 'PNG')


images = list(map(format, filenames))

progress.finish()
