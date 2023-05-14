import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

class MainScreen(Screen):
    def __init__(self, **kwargs):
       super(MainScreen, self).__init__(**kwargs)
       box = BoxLayout(orientation='vertical')
       box.add_widget(Label(text='Enter a topic:'))
       box.search = TextInput(multiline=False)
       box.add_widget(box.search)
       btn = Button(text='Search')
       btn.bind(on_press=self.callback)
       box.add_widget(btn)
       self.add_widget(box)

    def callback(self,*args):
       self.manager.current = 'eduscreen'

class EducationField(Screen):
    def __init__(self, **kwargs):
       super(EducationField, self).__init__(**kwargs)
       box = BoxLayout(orientation='vertical')
       box.add_widget(Label(text='What is your current level of education?'))
       dropdown = DropDown()
       for index in range(4):
           btn = Button(text ='value %d' % index, size_hint_y=None, height=44)
           btn.bind(on_release=lambda btn: dropdown.select(btn.text))
           dropdown.add_widget(btn)
       mainbutton = Button(text ='Education', size_hint =(None, None), pos =(350, 300))
       mainbutton.bind(on_release = dropdown.open)
       dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x))
       btn = Button(text='Next')
       btn.bind(on_press=self.callback)
       box.add_widget(btn)
       self.add_widget(box)

    def callback(self,*args):
       self.manager.current = 'mainscreen'
    

class MyApp(App):
    def build(self):
        manager = ScreenManager()
        mainscreen = MainScreen(name='mainscreen')
        eduscreen = EducationField(name='eduscreen')
        manager.add_widget(mainscreen)
        manager.add_widget(eduscreen)
        return manager
    

if __name__ == '__main__':
    MyApp().run()
