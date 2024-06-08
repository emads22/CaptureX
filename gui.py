from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from constants import KIVY_FILE


Builder.load_file(str(KIVY_FILE))


class CameraScreen(Screen):

    def start(self):
        print("EMAD")

    def stop(self):
        print("E>")


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
