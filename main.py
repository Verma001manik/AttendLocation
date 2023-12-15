from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
import sqlite3
from plyer import gps,notification
from kivy.clock import Clock
from kivy.utils import platform
import datetime

DATABASE_NAME = 'student.db'
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
            hint_text: '...'
            helper_text: 'Id'
            helper_text_mode: 'on_focus'
            readonly: True

        MDTextField:
            id: attendance_value
            input_type: 'number'
            hint_text: 'Attendance Id'
            helper_text: 'Enter attendance id'
            helper_text_mode: 'on_focus'
            readonly: True 

        MDRaisedButton:
            text: 'Mark Attendance'
            on_press: root.mark_attendance()
            size_hint_y: None
            height: dp(48)
'''


def logged_info(roll_number):
    if roll_number :
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT  is_logged_in FROM Students WHERE student_rollno COLLATE NOCASE =?", (roll_number,))
        logged_in  = cursor.fetchone()
        conn.close()
        print(logged_in[0])
        return logged_in[0]


        print(logged_in)

#Here We are decreasing the number of attendance attempts a student tend to mark . i:e 2 (each day )
        
def decrease_no_of_attempts(roll_number):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE Students SET attendance_attempts= attendance_attempts -1 WHERE student_rollno COLLATE NOCASE = ? ",(roll_number,))
    conn.commit()
    conn.close()
    print(" Decrease number of attempts ,!Done")

#Here we will reset the number of attempts = 2 after every 24 hours or after 8:30  - 9:00
    
def reset_no_of_attempts(roll_number):
    conn  = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE Students SET attendance_attempts=2 WHERE student_rollno COLLATE NOCASE = ? ",(roll_number,))
    conn.commit()
    conn.close()
    print(" Resetting  number of attempts ,!Done")

#Here we will get the number of remaining attempts for the student 
#Need to check everytime before marking the attendance
    
def get_attempts(roll_number):
    conn  = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT attendance_attempts FROM Students WHERE student_rollno COLLATE NOCASE =? ", (roll_number, ))
    attempts = cursor.fetchone()

    if attempts:
        print(attempts)
        print(attempts[0])
        return attempts[0]
    else:
        print("Error occured")

def changed_logged_in(roll_number):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        if logged_info(roll_number=roll_number)== 0:
            cursor.execute("UPDATE Students SET is_logged_in = 1 WHERE student_rollno COLLATE NOCASE =?", (roll_number,))        
            conn.commit()
            print(f"Student with roll number {roll_number} is now logged in.")
        else:
            cursor.execute("UPDATE Students SET is_logged_in = 0 WHERE student_rollno COLLATE NOCASE =?", (roll_number,))        
            conn.commit()
        
        conn.close()

class LoginScreen(Screen):
    def login(self):
        roll_number = self.ids.roll_number.text

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students WHERE student_rollno COLLATE NOCASE =?", (roll_number,))
        student = cursor.fetchone()

        conn.close()
        

        # Replace this with your actual login logic
        if student:
            # Remainder : remove ==1
            if logged_info(roll_number=roll_number)==0 :
                print(student)
                changed_logged_in(roll_number=roll_number)
                Snackbar(
                    text=f"Login successful : {student[1]}",
                    snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                    bg_color=(0, 1, 0, 1), 
                    
                        # Green color (RGBA)
                ).open()
                attendance_screen = self.manager.get_screen('attendance')
                attendance_screen.update_student_info(*student)
                self.manager.current = 'attendance'
            # self.manager.current = 'attendance'  # Redirect to Attendance screen
            else : 
                Snackbar(
                    text=f"Cannot login more than once ",
                    snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                    bg_color=(1, 0, 0, 1), 
                    
                        # Green color (RGBA)
                ).open()

        else:
            Snackbar(
                text="Login failed! Roll number is empty.",
                snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                bg_color=(1, 0, 0, 1),  # Red color (RGBA)
            ).open()

class AttendanceScreen(Screen):
    def __init__(self,**kwargs):
        super(AttendanceScreen,self).__init__(**kwargs)
        self._subject_code = '210188'
        self._attendance_id = 'Default'
    @property
    def subject_code(self):
        return self._subject_code

    @property
    def attendance_id(self):
        return self._attendance_id

    def update_student_info(self, student_id, roll_number, student_name, attendance_id, is_logged_in, attendance_attempts):
        self._subject_code = '210188'  # Set the default subject code
        self._attendance_id = attendance_id
        self.student_id = student_id  # Store student_id in the class
        self.roll_number = roll_number  # Store roll_number in the class
        self.student_name = student_name  # Store student_name in the class
        self.ids.subject_code.text = self.subject_code  # Update the subject code field
        self.ids.attendance_value.text = str(self.attendance_id)  # Update the attendance id field


    def mark_attendance(self):
        subject_code = self.ids.subject_code.text
        attendance_value = self.attendance_id

        # Replace this with your actual mark attendance logic
        if get_attempts(self.roll_number) >0:



            if subject_code and attendance_value:
                Snackbar(
                    text=f"Marking attendance for subject {subject_code} with value {attendance_value}",
                    snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                    bg_color=(0, 1, 0, 1),  # Green color (RGBA)
                ).open()
                decrease_no_of_attempts(self.roll_number)
                

                # self.request_location_permission()
            else:
                Snackbar(
                    text="Incomplete attendance details.",
                    snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                    bg_color=(1, 0, 0, 1),  # Red color (RGBA)
                ).open()
                # Call the method to get user location
        else:
             Snackbar(
                    text="Attendance already marked.",
                    snackbar_y=f"{Window.height - dp(48)}dp",  # At the top of the window
                    bg_color=(1, 0, 0, 1),  # Red color (RGBA)
                ).open()
             self.manager.current = 'login'

    # def get_user_location(self):
    #     if platform == 'android' or platform == 'ios':
    #         gps.configure(on_location=self.on_location)
    #         gps.start()
    #         Clock.schedule_once(lambda dt: gps.stop(), 20)  # Stop after 10 seconds

    # def on_location(self, **kwargs):
    #     lat = kwargs.get('lat', 'N/A')
    #     lon = kwargs.get('lon', 'N/A')
    #     print(lat,lon)
    #     Snackbar(
    #         text=f"Location: Latitude {lat}, Longitude {lon}",
    #         snackbar_y=f"{Window.height - dp(48)}dp",
    #         bg_color=(0, 1, 0, 1),
    #     ).open()
    # def request_location_permission(self):
    #     if platform == 'android' or platform == 'ios':
    #         permissions = gps.request_permissions()
    #         if permissions['location']:
    #             self.get_user_location()
    #         else:
    #             notification.notify(
    #                 title='Location Permission Required',
    #                 message='Please grant permission to access your location.',
    #             )
class MyApp(MDApp):
    def build(self):
        Window.size = (300, 500)
        return Builder.load_string(KV)

if __name__ == '__main__':
    MyApp().run()

