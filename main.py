from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
KV = '''
ScreenManager:
    LoginScreen:
        name: 'login'
    AttendanceScreen:
        name: 'attendance'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        size_hint_y: None
        height: self.minimum_height

        Label:
            text: 'Login Form'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(48)

        MDTextField:
            id: roll_number
            hint_text: 'Roll Number'
            helper_text: 'Enter your roll number'
            helper_text_mode: 'on_focus'

        MDRaisedButton:
            text: 'Login'
            on_press: root.login()
            size_hint_y: None
            height: dp(48)

<AttendanceScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        size_hint_y: None
        height: self.minimum_height

        Label:
            text: 'Mark Attendance'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(48)

        MDTextField:
            id: subject_code
            input_type: 'number'
            hint_text: 'Subject Code'
            helper_text: 'Enter subject code'
            helper_text_mode: 'on_focus'

        MDTextField:
            id: attendance_value
            input_type: 'number'
            hint_text: 'Attendance Value'
            helper_text: 'Enter attendance value'
            helper_text_mode: 'on_focus'

        MDRaisedButton:
            text: 'Mark Attendance'
            on_press: root.mark_attendance()
            size_hint_y: None
            height: dp(48)
'''

class LoginScreen(Screen):
    def login(self):
        roll_number = self.ids.roll_number.text

        # Replace this with your actual login logic
        if roll_number:
            Snackbar(
                text=f"Login successful for roll number: {roll_number}",
                snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                bg_color=(0, 1, 0, 1),  # Green color (RGBA)
            ).open()
            self.manager.current = 'attendance'  # Redirect to Attendance screen
        else:
            Snackbar(
                text="Login failed! Roll number is empty.",
                snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                bg_color=(1, 0, 0, 1),  # Red color (RGBA)
            ).open()

class AttendanceScreen(Screen):
    def mark_attendance(self):
        subject_code = self.ids.subject_code.text
        attendance_value = self.ids.attendance_value.text

        # Replace this with your actual mark attendance logic
        if subject_code and attendance_value:
            Snackbar(
                text=f"Marking attendance for subject {subject_code} with value {attendance_value}",
                snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                bg_color=(0, 1, 0, 1),  # Green color (RGBA)
            ).open()
        else:
            Snackbar(
                text="Incomplete attendance details.",
                snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                bg_color=(1, 0, 0, 1),  # Red color (RGBA)
            ).open()

class MyApp(MDApp):
    def build(self):
        Window.size = (300, 500)
        return Builder.load_string(KV)

if __name__ == '__main__':
    MyApp().run()
