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
    """Screen for displaying and controlling the camera feed."""

    def start(self):
        """Start the camera feed."""
        # Set the opacity of the camera widget to 1 to make it visible
        self.ids.camera.opacity = 1
        # Set the 'play' property of the camera widget to True to start the feed
        self.ids.camera.play = True
        self.ids.start_btn.text = "Stop Camera"  # Update button text
        # Set the texture of the camera widget to the current camera texture to display the feed
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stop the camera feed."""
        # Set the opacity of the camera widget to 0 to hide it
        self.ids.camera.opacity = 0
        # Set the 'play' property of the camera widget to False to stop the feed
        self.ids.camera.play = False
        self.ids.start_btn.text = "Start Camera"  # Update button text
        # Clear the camera feed display by setting its texture to None
        self.ids.camera.texture = None

    def capture(self):
        """Capture an image."""
        # Check if the camera feed is available and if the camera widget is currently visible
        if self.ids.camera._camera.texture and self.ids.camera.opacity == 1:

            # Generate a filename based on current time for the captured image
            current_time = time.strftime("%Y%m%d_%H%M%S")
            self.captured_img_path = str(
                CAPTURED_IMAGES / f'{current_time}.png')
            # Export the camera widget to a PNG file after ensuring the directory exists
            CAPTURED_IMAGES.mkdir(parents=True, exist_ok=True)
            self.ids.camera.export_to_png(self.captured_img_path)

            # Switch to the image screen after capturing the image
            self.manager.current = "image_screen"

            # Update the source of the image widget in the image screen to display the captured image
            self.manager.current_screen.ids.image.source = self.captured_img_path


class ImageScreen(Screen):
    """Screen for displaying captured images and managing sharing options."""

    link_message = "Create the image link first"

    def create_link(self):
        """Create a shareable link for the captured image."""
        # Get the path of the captured image from the camera screen
        img_path = App.get_running_app().root.ids.camera_screen.captured_img_path

        # Create a FileShare instance with the captured image path
        fileshare = FileShare(filepath=img_path)

        # Share the image and get the URL
        self.cap_img_url = fileshare.share()

        # Update the label with the image URL
        self.ids.link_label.text = self.cap_img_url

    def copy_link(self):
        """Copy the shareable link to the clipboard."""
        try:
            # Attempt to copy the URL to the clipboard
            Clipboard.copy(self.cap_img_url)
        except:
            # If an error occurs, update the label with a message
            self.ids.link_label.text = self.link_message

    def open_link(self):
        """Open the shareable link in the default web browser."""
        try:
            # Attempt to open the URL in the default web browser
            webbrowser.open(self.cap_img_url)
        except:
            # If an error occurs, update the label with a message
            self.ids.link_label.text = self.link_message

    def go_home(self):
        """Navigate back to the camera screen."""
        # Set the current screen to the camera screen, allowing the user to return to the camera feed screen
        self.manager.current = "camera_screen"


class RootWidget(ScreenManager):
    pass


class MainAppCam(App):
    """Main application class for the camera app."""

    def build(self):
        """Build the application."""
        return RootWidget()
