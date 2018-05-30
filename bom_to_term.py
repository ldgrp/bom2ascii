import image_to_ansi
import re
import requests
import time

from PIL import Image
from io import BytesIO

IDR = "023"
BASE_URL = "http://www.bom.gov.au/products/radar_transparencies/IDR{}.background.png"
LOOP_URL = "http://www.bom.gov.au/products/IDR{}.loop.shtml"

RESOLUTION = (100, 50)

def get_loop_image_urls(url):
    html = requests.get(url).text
    urls = re.findall(r'theImageNames\[\w\]\s=\s"(.+)"', html)
    return urls

def get_image_from_url(url, name):
    im_bytes = requests.get(url).content
    im = Image.open(BytesIO(im_bytes))
    im.save(name)
    return im

def process_background_image(image):
    WATER = '\u001b[34m.'
    LAND = '\u001b[37m\''

    # Warning: land/water is not guaranteed
    # TODO: find a better way to do this
    image = image.quantize(colors=2, method=0)
    img = image.resize(RESOLUTION)

    for x in range(img.size[1]):
        for y in range(img.size[0]):
            yield WATER if img.getpixel((y,x)) else LAND
        yield '\u001b[0m'

def process_loop_image(image):
    # image = image.quantize(colors=10, method=2)
    img = image
    img = image.resize(RESOLUTION)
    img = img.convert('RGBA')

    for x in range(img.size[1]):
        for y in range(img.size[0]):
            # TODO: stop being lazy and __actually__ crop the thing
            if x < 3 or x > img.size[1]-3:
                yield ''
                continue
            yield loop_color_to_ascii(img.getpixel((y, x)))
        yield '\033[0m\n'

# TODO: get rid of me
def loop_color_to_ascii(pixel):
    r, g, b, a = pixel

    if not a:
        return '\033[0m' 
    else:
        # TODO: don't be lazy
        short, rgb = image_to_ansi.rgb2short("%2x%2x%2x"%(r,g,b))
        return "\033[48;5;{}m".format(short)

if __name__ == "__main__":
    base_url = BASE_URL.format(IDR)
    loop_url = LOOP_URL.format(IDR)

    html = requests.get(loop_url).text
    text = re.findall(r'<title>(.+)</title>', html) 
    # Retrieve the background image
    bg_im = get_image_from_url(base_url, "IDR{}_bg.png".format(IDR))


    # Retrieve cloud boi images
    loop_image_urls = get_loop_image_urls(loop_url)
    loop_image_names = [image_url[28:] for image_url in loop_image_urls]

    loop_ims = []
    
    for image_url, image_name in zip(loop_image_urls, loop_image_names):
        loop_im = get_image_from_url(image_url, image_name)
        loop_ims.append(loop_im)

    i = 0
    while True:
        i += 1
        if i >= len(loop_ims):
            i = 0

        bg = process_background_image(bg_im)
        loop = process_loop_image(loop_ims[i])

        buf = ""
        for a, b in zip(bg, loop):
            buf += a+b

        print('\n'*50)
        print(text[0])
        print("="*len(text[0]))
        print(buf)
        time.sleep(1)
        
