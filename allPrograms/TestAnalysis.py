import csv
import os
import random
import sqlite3
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.resources import resource_add_path
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from plyer import filechooser


class LongRunningTaskPopup(Popup):
    def __init__(self, **kwargs):
        super(LongRunningTaskPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (600, 300)
        self.title = 'Loading...'
        self.content = Label(text='Please wait while the task is in progress')


class StudentButton(Button):
    pass


class MainScreen(Screen):
    s = []
    val = Widget()

    def file_chooser1(self):
        if App.get_running_app().s_0 == 'invalid input':
            App.get_running_app().s_0 = ''
        file = filechooser.open_file()
        if file == []:
            return None
        App.get_running_app().files += file
        App.get_running_app().s_0 += "".join(file).split("\\")[-1] + '\n'

    def show_loading_popup(self):
        loading_popup = LongRunningTaskPopup()  
        loading_popup.open()
        Clock.schedule_once(lambda x: self.Enter(loading_popup), 5)  

    def invalidinput(self):
        App.get_running_app().files = []
        Student_Selection.student = []
        conn = sqlite3.connect('KivyAppData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f'DROP TABLE {table[0]};')
        conn.commit()
        conn.close()

    def Enter(self, loading_popup):
        try:
            Student_Selection.getselfTL.clear_widgets()
        except:
            pass
        files = App.get_running_app().files
        Student_Selection.clear_widgets(self.val, children=None)
        try:
            if Student_Selection.student == []:
                if files == []:
                    App.get_running_app().s_0 = 'invalid input'
                cnn = sqlite3.connect("KivyAppData.db")
                cr = cnn.cursor()
                cr.execute("SELECT name FROM sqlite_master WHERE type='table';")
                table_names = cr.fetchall()
                for table in table_names:
                    cr.execute(f"DROP TABLE {table[0]}")
                for file in files:
                    if file[-4:] != ".csv":
                        App.get_running_app().s_0 = 'invalid input'
                        break
                    Marks = file[:-4][-3:]
                    if Marks.isidentifier():
                        with open(file, "r") as opfile:
                            rows = csv.reader(opfile)
                            header = next(rows)
                            for data in rows:  
                                Name = "_".join(data[0].split())
                                if file == files[0]:
                                    Student_Selection.student.append(data[0])
                                    if Name.isidentifier():
                                        cr.execute(f"create table {Name}{('Subjects', Marks)}")
                                    else:
                                        App.get_running_app().s_0 = 'invalid input'
                                        self.invalidinput()
                                        break
                                    column = []
                                    for number in range(1, len(data)):
                                        check = data[number].split("/")
                                        if check[0].isnumeric() and check[1].isnumeric():
                                            column.append((header[number], data[number]))
                                        else:
                                            App.get_running_app().s_0 = 'invalid input'
                                            self.invalidinput()
                                            break
                                    cr.executemany(f'insert into {Name}("Subjects","{Marks}") values(?,?)', column)
                                else:
                                    cr.execute(f"alter table {Name} add {Marks}")
                                    for number in range(1, len(data)):
                                        if check[0].isnumeric() and check[1].isnumeric():
                                            column.append((header[number], data[number]))
                                            cr.execute(
                                                f"update {Name} set {Marks}=\'{data[number]}\' where Subjects=\'{header[number]}\'")
                                        else:
                                            App.get_running_app().s_0 = 'invalid input'
                                            self.invalidinput()
                                            break
                    else:
                        App.get_running_app().s_0 = 'invalid input'  
                        self.invalidinput()
                        break
                loading_popup.dismiss()  
                Student_Selection.studentfunc(self.val)  
                if App.get_running_app().s_0 != 'invalid input':
                    App.get_running_app().sm.transition.direction = 'left'
                    App.get_running_app().sm.current = 'tablescreen'
                cnn.commit()
                cnn.close()
        except:
            App.get_running_app().s_0 = 'invalid input'
            self.invalidinput()
            loading_popup.dismiss()


class TableLabel(Label):
    pass


class TableScreen(Screen):
    def show_loading_popup(self):
        loading_popup = LongRunningTaskPopup()
        loading_popup.open()
        Clock.schedule_once(lambda x: self.backfunc(loading_popup), 5)

    def backfunc(self, loading_popup):
        App.get_running_app().s_0 = ''
        App.get_running_app().files = []
        Student_Selection.student = []
        conn = sqlite3.connect('KivyAppData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f'DROP TABLE {table_name};')
        conn.commit()
        conn.close()
        loading_popup.dismiss()


class Student_Selection(GridLayout):
    student = []
    getselfTL = 0
    parent = None
    previous_button = None

    def __init__(self, **kwargs):
        super(Student_Selection, self).__init__(**kwargs)
        MainScreen.val = self
        self.cols = len(self.student)
        self.bind(minimum_height=self.setter('height'))

    def studentfunc(self):
        for i in self.student:
            button = StudentButton(text=i, size_hint_y=None, height=35, on_release=self.Go_to_table,
                                   on_press=self.on_button_press)
            button.id = i
            self.add_widget(button)

    def Go_to_table(self, instance):
        Name = "_".join(instance.text.split())
        Tablelayout.table(self.getselfTL, txt=Name)

    def on_button_press(self, instance):
        if self.previous_button:
            self.previous_button.background_color = (0, 0, 0, 0)
        instance.background_color = (0, 0, 0, .3)
        self.previous_button = instance


class Tablelayout(GridLayout):
    def __init__(self, **kwargs, ):
        super(Tablelayout, self).__init__(**kwargs)
        Student_Selection.parent = self
        Student_Selection.getselfTL = self
        self.bind(minimum_height=self.setter('height'))

    def table(self, txt):
        cnn = sqlite3.connect("KivyAppData.db")
        cr = cnn.cursor()
        cr.execute(f"select * from {txt}")
        names = [d[0] for d in cr.description]
        self.cols = len(names)  
        rows = list(cr.fetchall())
        self.rows = len(rows) + 1  
        review_1 = ""
        subject = ""
        try:
            self.clear_widgets()
        except:
            pass
        for header in names:
            self.add_widget(TableLabel(text=header))
        self.max_subject = ""
        self.min_subject = ""
        for row in rows:
            increase = 0
            decrease = 0
            constant = 0
            subject = row[0]
            self.max_mark = row[1]
            self.min_mark = row[1]
            review_increase = [
                f"The student's performance in {subject} has improved.",
                f"{subject} performance is showing a positive trend.",
                f"In the subject of {subject}, the student's performance has risen.",
                f"{subject} performance is on the rise, exhibiting improvement.",
                f"The student has demonstrated improvement in {subject} performance.",
                f"{subject} proficiency has grown, showcasing enhancement.",
                f"A positive trend is evident in {subject} performance.",
                f"The student's mastery of {subject} has advanced.",
                f"{subject} scores have elevated, indicating improvement.",
                f"With a surge, the student has excelled in {subject} performance."
            ]
            review_decrease = [
                f"The student's performance in {subject} has declined.",
                f"{subject} performance is exhibiting a negative trend.",
                f"In the subject of {subject}, the student's performance has decreased.",
                f"{subject} performance is on the decline, showing a decrease.",
                f"The student's performance in {subject} has taken a downturn.",
                f"{subject} proficiency has decreased, indicating a decline.",
                f"A negative trend is evident in {subject} performance.",
                f"The student's mastery of {subject} has regressed.",
                f"{subject} scores have dropped, signaling a decrease.",
                f"With a decline, the student's performance in {subject} has weakened."
            ]
            review_constant = [
                f"The student's performance in {subject} remains consistent.",
                f"{subject} performance is stable, showing a consistent level of achievement.",
                f"In the subject of {subject}, the student's performance is steady.",
                f"{subject} performance has demonstrated a consistent level of proficiency.",
                f"The student has maintained a stable performance in {subject}.",
                f"{subject} proficiency is consistent, indicating a sustained level of achievement.",
                f"The student's performance in {subject} shows reliability and consistency.",
                f"{subject} scores have remained constant, reflecting a consistent performance.",
                f"With a consistent effort, the student excels in {subject} performance.",
                f"The subject of {subject} exhibits a consistently high level of performance."
            ]
            for index in range(len(row)):
                content = row[index]
                self.add_widget(TableLabel(text=content))
                if content != subject:
                    object_1 = int(content.split("/")[0])
                    if object_1 > int(self.max_mark.split("/")[0]):
                        self.max_mark = content
                        self.max_subject = subject
                    if object_1 < int(self.min_mark.split("/")[0]):
                        self.min_mark = content
                        self.min_subject = subject
                    if content != row[len(row) - 1]:
                        object_2 = int(row[index + 1].split("/")[0])
                        if object_2 > object_1:
                            increase += 1
                        elif object_2 < object_1:
                            decrease += 1
                        else:
                            constant += 1
            review_max = [
                f"The student has excelled to the maximum in {self.max_subject}.",
                f"In {self.max_subject}, the student has achieved the highest possible level of proficiency.",
                f"{self.max_subject} performance has reached the pinnacle with the student achieving the maximum.",
                f"The student has attained the maximum score in {self.max_subject}.",
                f"{self.max_subject} mastery is showcased as the student attains the maximum level of achievement.",
                f"In {self.max_subject}, the student's achievement has soared to the maximum.",
                f"The maximum level of proficiency in {self.max_subject} has been reached by the student.",
                f"{self.max_subject} scores reflect the student's attainment of the highest possible level.",
                f"The student has achieved the maximum in the subject of {self.max_subject}.",
                f"With outstanding performance, the student has reached the maximum in {self.max_subject}."
            ]
            review_min = [
                f"The student has scored the lowest in {self.min_subject}.",
                f"In {self.min_subject}, the student has attained the minimum level of proficiency.",
                f"{self.min_subject} performance has reached the lowest point with the student achieving the minimum.",
                f"The student has received the minimum score in {self.min_subject}.",
                f"{self.min_subject} mastery is at the lowest as the student attains the minimum level of achievement.",
                f"In {subject}, the student's achievement has fallen to the lowest.",
                f"The minimum level of proficiency in {self.min_subject} has been reached by the student.",
                f"{self.min_subject} scores reflect the student's attainment of the lowest possible level.",
                f"The student has achieved the lowest marks in the subject of {self.min_subject}.",
                f"With minimal performance, the student has reached the lowest in {self.min_subject}."
            ]
            if increase > decrease and increase > constant:
                review_1 += random.choice(review_increase) + " "
            elif decrease > increase and decrease > constant:
                review_1 += random.choice(review_decrease) + " "
            else:
                review_1 += random.choice(review_constant) + " "
        review_1 += random.choice(review_max) + " " + random.choice(review_min)
        App.get_running_app().review = review_1
        cnn.commit()
        cnn.close()


class TestAnalysis(App):
    review = StringProperty("")
    s_0 = StringProperty("")
    sm = ScreenManager()
    files = []

    def build(self):
        self.icon = "AppIcon.Ico"
        Builder.load_file("thelab.kv")
        self.sm.add_widget(MainScreen(name="mainscreen"))
        self.sm.add_widget(TableScreen(name="tablescreen"))
        return self.sm


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    TestAnalysis().run()
