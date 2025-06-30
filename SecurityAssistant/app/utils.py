from PIL import Image
from io import BytesIO

def load_image(file_bytes):
    return Image.open(BytesIO(file_bytes)).convert("RGB")
