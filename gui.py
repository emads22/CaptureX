import cv2
import time
import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.clipboard import Clipboard
from classes import FileShare
from constants import KIVY_FILE, DROIDCAM_URL, CAPTURED_IMAGES


# Load the Kivy file which contains the GUI layout
Builder.load_file(str(KIVY_FILE))


class CameraScreen(Screen):
    """Screen class for managing the camera feed."""

    def __init__(self, *args, **kwargs):
        """Initialize CameraScreen."""
        super().__init__(*args, **kwargs)
        self.video = None
        self.frame = None
        self.started = False
        self.captured_img_path = None

    def start(self):
        """Start or stop the video feed."""
        if self.started:
            # If the video feed is already started, stop it
            self.stop()
        else:
            # Otherwise, start the video feed
            self.ids.img_stream.opacity = 1  # Make the image stream visible
            # Change the button text to "Stop Camera"
            self.ids.start_btn.text = "Stop Camera"
            self.started = True  # Set the started flag to True

            try:
                # Open the video capture using the DroidCam URL
                self.video = cv2.VideoCapture(DROIDCAM_URL)
                if not self.video.isOpened():
                    # Raise an exception if the video feed cannot be opened
                    raise Exception("Unable to open DroidCam feed")

                # Schedule the update_frame method to be called every 1/30th of a second
                # This ensures that the video feed updates at approximately 30 frames per second (FPS)
                Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
            except Exception as e:
                # If an exception occurs, stop the video feed and display the error message
                self.stop(error_message=f'Error: "{e}"')
                return

    def stop(self, error_message=None):
        """Stop the video feed and clear resources."""
        # Hide the image stream
        self.ids.img_stream.opacity = 0
        # Change the button text back to "Start Camera"
        self.ids.start_btn.text = "Start Camera"

        # Stop frame retrieval by unscheduling the update_frame method
        Clock.unschedule(self.update_frame)

        # Release the video capture object if it exists
        if self.video:
            self.video.release()

        # Set the started flag to False indicating the camera feed is stopped
        self.started = False

        # If an error message is provided, print it to the console
        if error_message:
            print(f'\n\n--- {error_message} ---\n\n')

    def update_frame(self, delta_time):
        """
        Read a frame from the video feed and update the image.

        Args:
            delta_time (float): The time elapsed since the last call to this method.
                                This parameter is required by the Kivy Clock scheduler
                                to ensure smooth and consistent updates.
        """
        # Read a frame from the video capture object
        success, self.frame = self.video.read()
        if not success:
            # If reading a frame fails, stop the video feed and display an error message
            self.stop(
                error_message="Error: Failed to read frame from DroidCam feed")
            return

        # Convert the frame to a Kivy texture and update the Image widget
        self.ids.img_stream.texture = self._convert_frame_to_texture()

    def _convert_frame_to_texture(self):
        """Convert an OpenCV frame to a Kivy texture."""
        if self.frame is None:
            return None

        # Flip the frame vertically (since OpenCV and Kivy have different coordinate systems)
        self.frame = cv2.flip(self.frame, 0)

        # Create a Kivy texture with the same dimensions as the frame
        # The 'size' parameter takes the width and height of the frame
        # 'colorfmt' specifies the color format of the texture; 'bgr' is used since OpenCV uses BGR format
        texture = Texture.create(
            size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')

        # Convert the frame data to a byte string
        # This is necessary for transferring the image data into the Kivy texture
        buffer = self.frame.tobytes()

        # Blit (copy) the frame data onto the texture
        # 'Blit' is a term used in computer graphics to describe the process of transferring data from one buffer to another
        # 'colorfmt' specifies the color format of the input data; 'bgr' is used to match the frame data format
        # 'bufferfmt' specifies the format of the input data buffer; 'ubyte' is used for unsigned byte data
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        return texture

    def capture(self):
        """Capture an image."""
        # Check if a frame is available and if the image stream is currently visible
        if self.frame is not None and self.ids.img_stream.opacity == 1:

            # Get the current time to use as part of the image filename
            current_time = time.strftime("%Y%m%d_%H%M%S")

            # Construct the full path for the captured image
            self.captured_img_path = str(
                CAPTURED_IMAGES / f'{current_time}.png')

            # Ensure the directory for captured images exists
            CAPTURED_IMAGES.mkdir(parents=True, exist_ok=True)

            # Export the current frame as a PNG image to the specified path
            self.ids.img_stream.export_to_png(self.captured_img_path)
            # # Alternatively, we can use: cv2.imwrite()
            # cv2.imwrite(str(captured_img_path), self.frame)

            # Switch to the image screen after capturing the image
            self.manager.current = "image_screen"

            # Update the source of the image widget in the image screen to display the captured image
            self.manager.current_screen.ids.image.source = self.captured_img_path


class ImageScreen(Screen):
    """Screen class for managing captured images."""

    link_message = "Create the image link first"

    def create_link(self):
        """Create a shareable link for the captured image."""
        # Get the path of the captured image from the camera screen
        # This uses the App instance to access the root widget and the specific ID where the image path is stored
        img_path = App.get_running_app().root.ids.camera_screen.captured_img_path

        # Create a FileShare instance with the captured image path to handle the uploading/sharing of the image
        fileshare = FileShare(filepath=img_path)

        # Share the image and get the URL
        # The share method uploads the image and returns a URL for accessing it
        self.cap_img_url = fileshare.share()

        # Update the label with the image URL
        # This makes the URL visible in the UI, allowing the user to see the link
        self.ids.link_label.text = self.cap_img_url

    def copy_link(self):
        """Copy the image link to the clipboard."""
        try:
            # Attempt to copy the URL to the clipboard
            Clipboard.copy(self.cap_img_url)
        except:
            # If an error occurs, update the label with a message
            # This informs the user that the link needs to be created first
            self.ids.link_label.text = self.link_message

    def open_link(self):
        """Open the image link in the default web browser."""
        try:
            # Attempt to open the URL in the default web browser
            webbrowser.open(self.cap_img_url)
        except:
            # If an error occurs, update the label with a message
            # This informs the user that the link needs to be created first
            self.ids.link_label.text = self.link_message

    def go_home(self):
        """Navigate back to the camera screen."""
        # Set the current screen to the camera screen, by changing the current screen displayed by the ScreenManager to the camera screen, allowing the user to return to the screen where the camera feed is displayed.
        self.manager.current = "camera_screen"


class RootWidget(ScreenManager):
    """Root widget for managing screens."""


class MainApp(App):
    """Main application class."""

    def build(self):
        """Build the application."""
        return RootWidget()
