import cv2
import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from app_utils import get_droidcam_url
from constants import KIVY_FILE, NO_IMAGE_FILE, CAPTURED_IMAGES

Builder.load_file(str(KIVY_FILE))


class CameraScreen(Screen):

    def on_kv_post(self, base_widget):
        """Initialize variables after kv file is loaded."""
        self.ids.img_stream.source = str(NO_IMAGE_FILE)
        self.video = None
        self.frame = None
        self.started = False

    def start(self):
        """Start or stop the video feed."""
        if self.started:
            self.stop()
        else:
            self.ids.start_btn.text = "Stop Camera"
            self.started = True
            url = get_droidcam_url()  # Get the URL for the DroidCam server

            try:
                self.video = cv2.VideoCapture(url)
                if not self.video.isOpened():
                    raise Exception("Unable to open DroidCam feed")

                # Schedule the update_frame method to be called every 1/30th of a second
                Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
            except Exception as e:
                self.stop(
                    error_message=f'Error: "{e}"')
                return

    def stop(self, error_message=None):
        """Stop the video feed and clear resources."""
        # Stop frame retrieval of the scheduled updates
        Clock.unschedule(self.update_frame)
        if self.video:
            self.video.release()
        self.started = False
        self.ids.start_btn.text = "Start Camera"

        # Load and display the placeholder image
        self.frame = cv2.imread(str(NO_IMAGE_FILE))
        self.ids.img_stream.texture = self._convert_frame_to_texture()

        if error_message:
            print(f'\n\n--- {error_message} ---\n\n')

    def update_frame(self, delta_time):
        """Read a frame from the video feed and update the image."""
        success, self.frame = self.video.read()  # Read a frame from the video capture object
        if not success:
            self.stop(
                error_message="Error: Failed to read frame from DroidCam feed")
            return

        # Convert the frame to a Kivy texture and update the Image widget
        self.ids.img_stream.texture = self._convert_frame_to_texture()

    def _convert_frame_to_texture(self):
        """Convert an OpenCV frame to a Kivy texture."""
        if self.frame is None:
            return None
        
        # Flip the frame vertically
        self.frame = cv2.flip(self.frame, 0)

        # Create a Kivy texture with the same dimensions as the frame
        texture = Texture.create(
            size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')

        # Convert the frame data to a byte string
        buffer = self.frame.tobytes()

        # Blit the frame data onto the texture
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        return texture

    def capture(self):
        """Capture an image."""
        if self.frame is not None:
            current_time = time.strftime("%Y%m%d_%H%M%S")
            img_captured_path = CAPTURED_IMAGES / f'{current_time}.png'
            CAPTURED_IMAGES.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
            self.ids.img_stream.export_to_png(str(img_captured_path))

            # # Alternatively, we can use: cv2.imwrite()
            # cv2.imwrite(str(img_captured_path), self.frame)


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
