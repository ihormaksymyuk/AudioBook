from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from plyer import tts, filechooser

class TTSApp(App):
    def build(self):
        self.voice_list = ["Default", "Ukrainian", "English", "Other"]  # Плейсхолдер

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.info_label = Label(text='Введіть текст або відкрийте файл:')
        layout.add_widget(self.info_label)

        self.text_input = TextInput(multiline=True, size_hint_y=0.5)
        layout.add_widget(self.text_input)

        # Кнопка відкриття файлу
        button_open = Button(text='📂 Відкрити .txt файл')
        button_open.bind(on_press=self.open_file)
        layout.add_widget(button_open)

        # Вибір голосу (візуальний елемент)
        self.voice_spinner = Spinner(text="Default", values=self.voice_list)
        layout.add_widget(self.voice_spinner)

        # Повзунок швидкості
        self.speed_label = Label(text='Швидкість озвучки: 1.0')
        layout.add_widget(self.speed_label)

        self.speed_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.1)
        self.speed_slider.bind(value=self.update_speed)
        layout.add_widget(self.speed_slider)

        # Кнопка озвучення
        speak_button = Button(text='🔊 Озвучити текст')
        speak_button.bind(on_press=self.speak_text)
        layout.add_widget(speak_button)

        # Кнопка "зберегти"
        save_button = Button(text='💾 Зберегти аудіо (імітація)')
        save_button.bind(on_press=self.save_audio)
        layout.add_widget(save_button)

        # Статус
        self.status = Label(text='')
        layout.add_widget(self.status)

        return layout

    def open_file(self, instance):
        filechooser.open_file(on_selection=self.load_file, filters=["*.txt"])

    def load_file(self, selection):
        if selection:
            try:
                with open(selection[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_input.text = content
                    self.status.text = '✅ Файл завантажено'
            except Exception as e:
                self.status.text = f'❌ Помилка при відкритті: {str(e)}'

    def update_speed(self, instance, value):
        self.speed_label.text = f"Швидкість озвучки: {round(value, 1)}"

    def speak_text(self, instance):
        text = self.text_input.text.strip()
        rate = self.speed_slider.value
        if text:
            try:
                tts.speak(text=text, rate=rate)
                self.status.text = '✅ Текст озвучено'
            except Exception as e:
                self.status.text = f'❌ Помилка: {str(e)}'
        else:
            self.status.text = '⚠️ Введіть текст'

    def save_audio(self, instance):
        # Плейсхолдер: можна інтегрувати з сервером або Android TTS file API
        self.status.text = "📥 Збереження в аудіофайл ще не реалізоване."

if __name__ == '__main__':
    TTSApp().run()
