import time
import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from classes import FileShare
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
            self.captured_img_path = str(CAPTURED_IMAGES / f'{current_time}.png')
            # Export the camera widget to a PNG file
            self.ids.camera.export_to_png(self.captured_img_path)

            self.manager.current = "image_screen"

            self.manager.current_screen.ids.image.source = self.captured_img_path


class ImageScreen(Screen):

    link_message = "Create the image link first"

    def create_link(self):
        img_path = App.get_running_app().root.ids.camera_screen.captured_img_path

        fileshare = FileShare(filepath=img_path)

        self.cap_img_url = fileshare.share()

        self.ids.link_label.text = self.cap_img_url

    def copy_link(self):
        try:
            Clipboard.copy(self.cap_img_url)
        except:
            self.ids.link_label.text = self.link_message

    def open(self):
        try:
            webbrowser.open(self.cap_img_url)
        except:
            self.ids.link_label.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
