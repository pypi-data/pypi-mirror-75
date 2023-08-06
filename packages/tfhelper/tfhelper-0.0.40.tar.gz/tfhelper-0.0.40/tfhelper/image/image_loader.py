from PIL import Image


def image_loader(path, convert_rgb=True):
    image = Image.open(path).convert("RGB")
    