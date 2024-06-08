import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from constants import KIVY_FILE_CAM, CAPTURED_IMAGES

# Load the KV file that defines the UI layout for the CameraScreen
Builder.load_file(str(KIVY_FILE_CAM))

class CameraScreen(Screen):

    def start(self):
        """Start the camera feed."""
        # Set the 'play' property of the camera widget to True to start the feed
        self.ids.camera.play = True
        self.ids.start_btn.text = "Stop Camera"  # Update button text
        self.ids.camera.texture = self.ids.camera._camera.texture  # Display camera feed

    def stop(self):
        """Stop the camera feed."""
        # Set the 'play' property of the camera widget to False to stop the feed
        self.ids.camera.play = False
        self.ids.start_btn.text = "Start Camera"  # Update button text
        self.ids.camera.texture = None  # Clear the camera feed display

    def capture(self):
        """Capture an image."""
        # Check if the camera feed is available
        if self.ids.camera._camera.texture:
            # Generate a filename based on current time for the captured image
            current_time = time.strftime("%Y%m%d_%H%M%S")
            img_captured_path = CAPTURED_IMAGES / f'{current_time}.png'
            # Export the camera widget to a PNG file
            self.ids.camera.export_to_png(str(img_captured_path))

class ImageScreen(Screen):

    def create_link(self):
        pass

    def copy(self):
        pass

    def open(self):
        pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()
