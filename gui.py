from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from constants import KIVY_FILE


Builder.load_file(str(KIVY_FILE))


class FirstScreen(Screen):
    def sla(self):
        print("EMAD")


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
