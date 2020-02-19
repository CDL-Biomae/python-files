import kivy
from kivy.app import App
from kivy.uix.button import  Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from report import main
 
class QueryApp(App):
 
    def build(self):
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.query = TextInput(hint_text='Write here', size_hint=(.5,.2))
        self.btn = Button(text='Reset', on_press=self.clearText, size_hint=(.1,.2))
        self.main = Button(text='Go', on_press=self.main_is_possible, size_hint=(.1,.2))
        self.box.add_widget(self.query)
        self.box.add_widget(self.btn)
        self.box.add_widget(self.main)
        return self.box
 
    def clearText(self, instance):
        self.query.text = ''
    
    def main_is_possible(self,instance):
        if self.query.text!='' and self.query.text!=None:
            main([self.query.text])

class Excel_CreatorApp(App):
    def build(self):
        return QueryApp()


if __name__ == "__main__":
    QueryApp().run()
