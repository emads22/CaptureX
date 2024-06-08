import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

# Get the IP address and port number of the DroidCam server from environment variables
DROIDCAM_IP_ADDRESS = os.getenv('DROIDCAM_IP_ADDRESS')
DROIDCAM_PORT_NUMBER = os.getenv('DROIDCAM_PORT_NUMBER')
FILESTACK_API_KEY = os.getenv('FILESTACK_API_KEY')
ASSETS = Path("./assets")
CAPTURED_IMAGES = ASSETS / "captured_images"
TEMP_IMAGES = ASSETS / "temp_images"
NO_IMAGE_FILE = CAPTURED_IMAGES / "not_available.jpg"
KIVY_FILE = ASSETS / "data" / "front_end.kv"
KIVY_FILE_CAM = ASSETS / "data" / "front_end_cam.kv"