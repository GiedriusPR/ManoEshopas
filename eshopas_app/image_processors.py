from imagekit.processors import ResizeToFill
from PIL import Image

class ResizeImageProcessor(ResizeToFill):
    width = 150
    height = 200
    upscale = False