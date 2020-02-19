import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from report import main

from kivy.core.window import Window


class QueryApp(App):

    def build(self):
        Window.clearcolor = (0.29, 0.549, 0.792, 1)  # Bleu clair de Biomae
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.query = TextInput(hint_text='Write here', size_hint=(.5, .2))
        self.btn = Button(
            text='Reset', on_press=self.clearText, size_hint=(.1, .2))
        self.btn.background_color = (
            0.004, 0.314, 0.624, 1)  # Bleu foncé Biomae
        self.main = Button(
            text='Go', on_press=self.main_is_possible, size_hint=(.1, .2))
        self.main.background_color = (0.004, 0.314, 0.624, 1)
        self.box.add_widget(self.query)
        self.box.add_widget(self.btn)
        self.box.add_widget(self.main)
        return self.box

    def clearText(self, instance):
        self.query.text = ''

    def main_is_possible(self, instance):
        if self.query.text != '':
            main([self.query.text])


class Excel_CreatorApp(App):
    def build(self):
        return QueryApp()


if __name__ == "__main__":
    QueryApp().run()
