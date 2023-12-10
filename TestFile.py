from tkinter import *
import sqlite3
from tkinter import messagebox
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel, Label, Button, Text, Scrollbar
from PIL import Image, ImageTk
from openai import ChatCompletion


    


class NursePage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('800x600')
        self.window.title('Nurse Page')
        self.nurse_label = Label(self.window, text="Welcome, Nurse!", font=("yu gothic ui", 20, "bold"))
        self.nurse_label.pack(pady=50)
        self.analyze_button = Button(self.window, text="Analyze Patients", command=self.analyze_patient_data, font=("yu gothic ui", 13, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.analyze_button.pack(pady=20)
        self.sign_out_button = Button(self.window, text="Sign Out", command=self.sign_out, font=("yu gothic ui", 13, "bold"), bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.sign_out_button.pack(pady=20)

        self.camera = cv.VideoCapture(0)
        self.last_frame = None
        self.motion_detected = False

        self.sketch_canvas = Canvas(self.window, width=640, height=480)
        self.sketch_canvas.pack()

        self.update_camera()

    def analyze_patient_data(self):
        graph_window = Toplevel(self.window)
        graph_window.title("Live Motion Graph")

        graph_frame = Frame(graph_window)
        graph_frame.pack()

        fig_graph, ax_graph = plt.subplots()
        line_graph, = ax_graph.plot([], [], label='Live Graph')
        ax_graph.legend()
        ax_graph.set_xlabel('Time')
        ax_graph.set_ylabel('Pixel Value')

        times_graph = []
        pixel_data = []

        canvas = FigureCanvasTkAgg(fig_graph, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        def update_graph():
            nonlocal times_graph, pixel_data

            ret, frame = self.camera.read()
            if ret:
                gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                pixel_values = gray_frame[gray_frame.shape[0] // 2, :]

                times_graph.append(len(times_graph) + 1)
                pixel_data.append(pixel_values.mean())

                line_graph.set_data(times_graph, pixel_data)
                ax_graph.relim()
                ax_graph.autoscale_view()

                canvas.draw()
                canvas.flush_events()

                if self.detect_fast_motion(frame):
                    if not self.motion_detected:
                        self.motion_detected = True
                        messagebox.showwarning("Fast Motion Detected", "Check on your patient!")
                else:
                    self.motion_detected = False

            graph_window.after(10, update_graph)

        update_graph()

    def detect_fast_motion(self, frame):
        if self.last_frame is None:
            self.last_frame = frame
            return False

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        blurred = cv.GaussianBlur(gray, (5, 5), 0)

        frame_delta = cv.absdiff(self.last_frame, frame)
        gray_delta = cv.cvtColor(frame_delta, cv.COLOR_BGR2GRAY)

        _, thresh = cv.threshold(gray_delta, 145, 255, cv.THRESH_BINARY)  

        thresh = cv.dilate(thresh, None, iterations=2)
        contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        super_speed_motion_detected = any(
            cv.contourArea(contour) > 225 and cv.norm(cv.minAreaRect(contour)[1]) > 100
            for contour in contours
        )

        self.last_frame = frame

        return super_speed_motion_detected

    def apply_sketch_effect(self, frame):
        height, width, _ = frame.shape
        resized_image = cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpen_image = cv.filter2D(resized_image, -1, kernel)

        gray = cv.cvtColor(sharpen_image, cv.COLOR_BGR2GRAY)
        inverse_image = 255 - gray
        blured_image = cv.GaussianBlur(inverse_image, (15, 15), 0, 0)
        pencil_sketch = cv.divide(gray, 255 - blured_image, scale=256)

        return pencil_sketch

    def sign_out(self):
        self.camera.release()
        self.window.destroy()

    def update_camera(self):
        ret, frame = self.camera.read()
        if ret:
            pencil_sketch = self.apply_sketch_effect(frame)
            img = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(pencil_sketch, cv.COLOR_BGR2RGB)))
            self.sketch_canvas.create_image(0, 0, anchor=NW, image=img)
            self.sketch_canvas.img = img  

        self.window.after(10, self.update_camera)
    

class PatientsPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('800x600')
        self.window.title('Patients Page')

        bg_image = Image.open('background1.png')
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.window, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.patients_label = Label(self.window, text="Welcome to Patients Page!", font=("yu gothic ui", 20, "bold"), bg='#040405', fg='white')
        self.patients_label.pack(pady=50)

        self.sign_out_button = Button(self.window, text="Sign Out", command=self.sign_out, font=("yu gothic ui", 13, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.sign_out_button.pack(pady=20)

        self.reminder_button = Button(self.window, text="Open Reminder App", command=self.open_reminder_app, font=("yu gothic ui", 13, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.reminder_button.pack(pady=20)

        self.questions_button = Button(self.window, text="Questions", command=self.open_questions, font=("yu gothic ui", 13, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.questions_button.pack(pady=20)

        self.reminder_button = Button(self.window, text="Open Reminder App", command=self.open_reminder_app,
        font=("yu gothic ui", 13, "bold"), bg='#4CAF50', cursor='hand2',
        activebackground='#45a049', fg='white')
        self.reminder_button.pack(pady=20)

    def open_reminder_app(self):
        reminder_window = Toplevel(self.window)
        ReminderApp(reminder_window)

    def open_reminder_app(self):
        reminder_window = Toplevel(self.window)
        ReminderApp(reminder_window)

    def open_questions(self):
        questions_window = Toplevel(self.window)
        QuestionsPage(questions_window)

    def sign_out(self):
        self.window.destroy()

class QuestionsPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('400x400')
        self.window.title('Questions Page')

        self.questions_label = Label(self.window, text="ChatGPT api !", font=("yu gothic ui", 20, "bold"))
        self.questions_label.pack(pady=10)

        self.chat_history = Text(self.window, wrap="word", width=40, height=10, font=("yu gothic ui", 12))
        self.chat_history.pack(pady=10, padx=10)

        self.scrollbar = Scrollbar(self.window, command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        self.input_label = Label(self.window, text="Your Question:", font=("yu gothic ui", 12))
        self.input_label.pack(pady=5)

        self.input_text = Text(self.window, wrap="word", width=40, height=2, font=("yu gothic ui", 12))
        self.input_text.pack(pady=5, padx=10)

        self.submit_button = Button(self.window, text="Submit", command=self.submit_question, font=("yu gothic ui", 12, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.submit_button.pack(pady=10)

        self.close_button = Button(self.window, text="Close", command=self.close_questions, font=("yu gothic ui", 12, "bold"), bg='#4CAF50', cursor='hand2', activebackground='#45a049', fg='white')
        self.close_button.pack(pady=5)

    def submit_question(self):
        user_question = self.input_text.get("1.0", "end-1c")
        response = self.get_gpt3_response(user_question)
        self.chat_history.insert("end", f"User: {user_question}\nGPT-3: {response}\n\n")
        self.input_text.delete("1.0", "end")

    def close_questions(self):
        self.window.destroy()

    def get_gpt3_response(self, user_input):
        api_key = 'YOUR_API_KEY'
        openai.api_key = api_key

        prompt = f"User: {user_input}\nGPT-3:"
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        return response['choices'][0]['message']['content']
class ReminderApp:
    def __init__(self, reminder_window):
        self.reminder_window = reminder_window
        self.reminder_window.title("Reminder App")

        self.drug_label = Label(self.reminder_window, text="Drug:")
        self.drug_label.pack(pady=10)
        
        self.patient_label = Label(self.reminder_window, text="Patient:")
        self.patient_label.pack(pady=10)
        
        self.dose_label = Label(self.reminder_window, text="Dose:")
        self.dose_label.pack(pady=10)
        
        self.time_label = Label(self.reminder_window, text="Time:")
        self.time_label.pack(pady=10)

        self.drug_entry = Entry(self.reminder_window)
        self.drug_entry.pack(pady=10)
        
        self.patient_entry = Entry(self.reminder_window)
        self.patient_entry.pack(pady=10)
        
        self.dose_entry = Entry(self.reminder_window)
        self.dose_entry.pack(pady=10)
        
        self.time_entry = Entry(self.reminder_window)
        self.time_entry.pack(pady=10)

        self.submit_button = Button(self.reminder_window, text="Submit", command=self.submit_action)
        self.submit_button.pack(pady=10)

    def submit_action(self):
        drug = self.drug_entry.get()
        patient = self.patient_entry.get()
        dose = self.dose_entry.get()
        time = self.time_entry.get()

        if not drug or not patient or not dose or not time:
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        # Add your logic for handling the reminder details (drug, patient, dose, time) here

        # You may want to use the information (drug, patient, dose, time) to set reminders or perform other actions.
        # For now, we'll just print the details.
        print(f"Drug: {drug}, Patient: {patient}, Dose: {dose}, Time: {time}")

        # Close the reminder window after submission
        self.reminder_window.destroy()

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')
        self.bg_frame = Image.open('background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405", fg='white', bd=5, relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)
        self.side_image = Image.open('vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)
        self.sign_in_image = Image.open('hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white", font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)
        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)
        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        self.username_icon = Image.open('username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)
        self.lgn_button = Image.open('btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.login_action)
        self.login.place(x=20, y=10)
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?", font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT, activebackground="#040405", borderwidth=0, background="#040405", cursor="hand2")
        self.forgot_button.place(x=630, y=510)
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"), relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)
        self.signup_img = ImageTk.PhotoImage(file='register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2", borderwidth=0, background="#040405", activebackground="#040405", command=self.signup)
        self.signup_button_label.place(x=670, y=555, width=111, height=35)
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)
        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)
        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        self.password_icon = Image.open('password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        self.show_image = ImageTk.PhotoImage(file='show.png')
        self.hide_image = ImageTk.PhotoImage(file='hide.png')
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def signup(self):
        signup_window = Toplevel(self.window)
        signup_window.title("Sign Up")
        signup_window.geometry("400x200")
        username_label = Label(signup_window, text="Username:")
        username_label.pack(pady=10)
        username_entry = Entry(signup_window)
        username_entry.pack(pady=10)
        password_label = Label(signup_window, text="Password:")
        password_label.pack(pady=10)
        password_entry = Entry(signup_window, show="*")
        password_entry.pack(pady=10)
        signup_button = Button(signup_window, text="Sign Up", command=lambda: self.add_user(username_entry.get(), password_entry.get()))
        signup_button.pack(pady=10)

    def add_user(self, username, password):
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password.")
            return
        try:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User successfully registered.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password.")
            return
        try:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                if password == "nurse1234":
                    self.open_nurse_page()
                else:
                    self.open_patients_page()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def open_nurse_page(self):
        self.window.withdraw()
        nurse_window = Toplevel(self.window)
        NursePage(nurse_window)

    def open_patients_page(self):
        self.window.withdraw()
        patients_window = Toplevel(self.window)
        PatientsPage(patients_window)

if __name__ == '__main__':
    window = Tk()
    LoginPage(window)
    window.mainloop()