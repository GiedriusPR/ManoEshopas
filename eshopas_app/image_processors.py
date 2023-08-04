from imagekit.processors import ResizeToFill

class ResizeImageProcessor(ResizeToFill):
    width = 150
    height = 200
    upscale = False

class ResizeProfilePictureinCommentProcessor(ResizeToFill):
    width = 40
    height = 40
    upscale = False