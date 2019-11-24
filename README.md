# alt-spelling

Install dependencies:

```
pipenv install
```

Run the script:

```
$ pipenv run python3 script.py --help
```

```
usage: script.py [-h] [--width WIDTH] [--height HEIGHT] [--size SIZE]
                 [--dpi DPI] [--anchor ANCHOR] [--filename FILENAME]
                 [--dir DIR] [--hue HUE]

optional arguments:
  -h, --help           show this help message and exit
  --width WIDTH        Target width in inches
  --height HEIGHT      Target height in inches
  --size SIZE          Size in pixels to slice tiles
  --dpi DPI            Target dots per inch
  --anchor ANCHOR      Crop anchor position
  --filename FILENAME  Output filename
  --dir DIR            Directory to process
  --hue HUE            Rotate hues
```

Example:

```
$ pipenv run python3 script.py --width=30 --height=36 --dir=source/example/*.jpg
# => Cropping ████████████████████████████████ 100%
# => Building map...
# => Building output...
# => Processing ████████████████████████████████ 100%
# => Saving...
# => Done.
```
