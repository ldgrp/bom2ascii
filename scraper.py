import re
import requests

from io import BytesIO
from PIL import Image
from image_processing import process_background_image, process_loop_image

BG_URL = "http://www.bom.gov.au/products/radar_transparencies/IDR{}.background.png"
LOOP_URL = "http://www.bom.gov.au/products/IDR{}.loop.shtml"

def get_image_from_url(url, name=None):
    """(Image) Retrieves the Image at a given 'url'. If 'name' 
    is specified, the image is saved with filename 'name'"""
    im_bytes = requests.get(url).content
    im = Image.open(BytesIO(im_bytes))

    if name:
        im.save(name)

    return im

def get_radar(idr, resolution=(100, 50)):
    bg_url = BG_URL.format(idr)
    loop_url = LOOP_URL.format(idr)


    # Retrieve the background image
    bg_im = get_image_from_url(bg_url)

    # Retrieve cloud boi images
    loop_html = requests.get(loop_url).text
    title = re.findall(r'<title>(.+)</title>', loop_html)[0]
    im_urls = re.findall(r'theImageNames\[\w\]\s=\s"(.+)"', loop_html)

    loop_ims = []

    for im_url in im_urls:
        loop_im = get_image_from_url(im_url)
        loop_ims.append(loop_im)

    # Image -> Generator
    # bg_ascii_generator = process_background_image(bg_im, resolution)
    loop_asciis_generator = [process_loop_image(loop_im, resolution) for loop_im in loop_ims]

    # Generator -> String
    loop_asciis = []
    
    for item in loop_asciis_generator:
        buf = ""
        # TODO: wtf u lazy fuk
        bg_ascii_generator = process_background_image(bg_im, resolution)
        for x, y in zip(bg_ascii_generator, item):
            buf += x+y
        loop_asciis.append(buf)

    return loop_asciis, title

if __name__ == "__main__":
    from itertools import cycle
    import time

    idr = "023"
    resolution = (100, 50)

    text_list, title = get_radar(idr, resolution)

    text_cycle = cycle(text_list)

    for item in text_cycle:
        print('\n'*20)
        print(title)
        print(item)
        time.sleep(1)
        

    
    




