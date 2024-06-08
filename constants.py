import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

FILESTACK_API_KEY = os.getenv('FILESTACK_API_KEY')
ASSETS = Path("./assets")
IMAGES = ASSETS / "images"
NO_IMAGE_FILE = IMAGES / "not_available.jpg"
KIVY_FILE = ASSETS / "data" / "front_end.kv"