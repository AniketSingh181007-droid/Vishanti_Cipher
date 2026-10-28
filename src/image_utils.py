from PIL import Image
import numpy as np
import os

def load_image(path):
    with Image.open(path) as image:
        image = image.convert("RGB")
        return np.array(image, dtype=np.uint8)


def save_image(image, path):
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)

    output = Image.fromarray(image)
    output.save(path, format="PNG")