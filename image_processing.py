"""Processes images to ASCII"""
import image_to_ansi

def process_background_image(image, resolution):
    """(Generator) Converts an Image to ASCII"""
    WATER = "\u001b[34m."
    LAND = "\u001b[37m'"

    # Warning: land/water is not guaranteed
    # TODO: you disgusting pleb, fix me
    image = image.quantize(colors=2, method=0)
    image = image.resize(resolution)

    for x in range(image.size[1]):
        for y in range(image.size[0]):
            yield WATER if image.getpixel((y, x)) else LAND # eww
        yield '\u001b[0m'

def process_loop_image(image, resolution):
    """(Generator) Returns a generator of strings"""
    image = image.resize(resolution)
    image = image.convert('RGBA')

    for x in range(image.size[1]):
        for y in range(image.size[0]):
            # TODO: stop being lazy and *actually* crop the image
            if x < 3 or x > image.size[1]-3:
                yield ''
                continue
            yield pixel_to_ascii(image.getpixel((y, x)))
        yield '\033[0m\n'

# TODO: get rid of me
def pixel_to_ascii(pixel):
    r, g, b, a = pixel

    if not a:
        return '\033[0m'
    else:
        # TODO: dont be lazy
        short, rgb = image_to_ansi.rgb2short("%2x%2x%2x"%(r,g,b))
        return "\033[48;5;{}m".format(short)


