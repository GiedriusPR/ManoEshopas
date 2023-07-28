from imagekit.processors import ResizeToFill

# Custom processor to resize the image to a specific size
class ResizeImageProcessor(ResizeToFill):
    width = 150
    height = 200
    upscale = False