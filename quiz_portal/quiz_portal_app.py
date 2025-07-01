import tkinter as tk
from tkinter import ttk, messagebox
import random

# Sample questions for each level (PYQs style)
CHEMISTRY_QUESTIONS = [
    {
        'question': 'What is the atomic number of carbon?',
        'options': ['6', '8', '12', '14'],
        'answer': 0
    },
    {
        'question': 'Which of the following is a noble gas?',
        'options': ['Oxygen', 'Nitrogen', 'Argon', 'Hydrogen'],
        'answer': 2
    },
    {
        'question': 'The chemical formula of washing soda is?',
        'options': ['Na2CO3', 'NaHCO3', 'CaCO3', 'K2CO3'],
        'answer': 0
    },
    {
        'question': 'Who is known as the father of modern chemistry?',
        'options': ['Lavoisier', 'Dalton', 'Mendeleev', 'Rutherford'],
        'answer': 0
    },
    {
        'question': 'Which acid is present in lemon?',
        'options': ['Acetic acid', 'Citric acid', 'Sulphuric acid', 'Hydrochloric acid'],
        'answer': 1
    },
    {
        'question': 'Which of the following is an exothermic process?',
        'options': ['Evaporation', 'Sublimation', 'Condensation', 'Melting'],
        'answer': 2
    },
    {
        'question': 'The pH of pure water at 25°C is?',
        'options': ['7', '5', '9', '6'],
        'answer': 0
    },
    {
        'question': 'Which metal is stored in kerosene?',
        'options': ['Sodium', 'Iron', 'Copper', 'Aluminium'],
        'answer': 0
    },
    {
        'question': 'Which gas is evolved when zinc reacts with dilute H2SO4?',
        'options': ['Oxygen', 'Hydrogen', 'Nitrogen', 'Chlorine'],
        'answer': 1
    },
    {
        'question': 'Which of the following is a greenhouse gas?',
        'options': ['O2', 'CO2', 'N2', 'He'],
        'answer': 1
    },
]

PHYSICS_QUESTIONS = [
    {
        'question': 'What is the SI unit of force?',
        'options': ['Joule', 'Newton', 'Pascal', 'Watt'],
        'answer': 1
    },
    {
        'question': 'Who discovered the law of gravitation?',
        'options': ['Newton', 'Einstein', 'Galileo', 'Faraday'],
        'answer': 0
    },
    {
        'question': 'The speed of light in vacuum is?',
        'options': ['3x10^8 m/s', '3x10^6 m/s', '3x10^5 m/s', '3x10^7 m/s'],
        'answer': 0
    },
    {
        'question': 'Which instrument is used to measure electric current?',
        'options': ['Voltmeter', 'Ammeter', 'Barometer', 'Hygrometer'],
        'answer': 1
    },
    {
        'question': 'Which mirror is used in vehicles as rear view mirror?',
        'options': ['Concave', 'Convex', 'Plane', 'None'],
        'answer': 1
    },
    {
        'question': 'The unit of power is?',
        'options': ['Joule', 'Watt', 'Newton', 'Pascal'],
        'answer': 1
    },
    {
        'question': 'Which law states that current is directly proportional to voltage?',
        'options': ["Ohm's Law", "Newton's Law", "Faraday's Law", "Hooke's Law"],
        'answer': 0
    },
    {
        'question': 'What is the acceleration due to gravity on Earth?',
        'options': ['9.8 m/s^2', '8.9 m/s^2', '10.8 m/s^2', '7.8 m/s^2'],
        'answer': 0
    },
    {
        'question': 'Which of the following is a vector quantity?',
        'options': ['Speed', 'Distance', 'Displacement', 'Work'],
        'answer': 2
    },
    {
        'question': 'Which color of light has the shortest wavelength?',
        'options': ['Red', 'Blue', 'Green', 'Violet'],
        'answer': 3
    },
]

MATH_QUESTIONS = [
    {
        'question': 'What is the value of π (pi) up to two decimal places?',
        'options': ['3.12', '3.14', '3.16', '3.18'],
        'answer': 1
    },
    {
        'question': 'The solution of the equation x^2 - 4 = 0 is?',
        'options': ['x=2', 'x=-2', 'x=2 or -2', 'x=4'],
        'answer': 2
    },
    {
        'question': 'What is the derivative of x^2?',
        'options': ['2x', 'x', 'x^2', '2'],
        'answer': 0
    },
    {
        'question': 'The sum of angles in a triangle is?',
        'options': ['90°', '180°', '270°', '360°'],
        'answer': 1
    },
    {
        'question': 'What is the next prime number after 7?',
        'options': ['9', '10', '11', '13'],
        'answer': 2
    },
    {
        'question': 'If sin θ = 1, then θ = ?',
        'options': ['0°', '30°', '90°', '180°'],
        'answer': 2
    },
    {
        'question': 'What is 15% of 200?',
        'options': ['20', '25', '30', '35'],
        'answer': 2
    },
    {
        'question': 'The value of log(1) is?',
        'options': ['0', '1', '10', 'Undefined'],
        'answer': 0
    },
    {
        'question': 'What is the square root of 144?',
        'options': ['10', '11', '12', '13'],
        'answer': 2
    },
    {
        'question': 'If a triangle has sides 3, 4, 5, it is a?',
        'options': ['Equilateral', 'Isosceles', 'Scalene', 'Right-angled'],
        'answer': 3
    },
]

# Combine all questions into one list
ALL_QUESTIONS = CHEMISTRY_QUESTIONS + PHYSICS_QUESTIONS + MATH_QUESTIONS

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Quiz Portal')
        self.root.geometry('950x700')
        self.root.resizable(False, False)
        self.root.configure(bg='#2d084f')
        self.reset_quiz()
        self.create_widgets()
        self.show_question()

    def reset_quiz(self):
        self.question_index = 0
        self.selected_answers = [None] * 30
        self.score = 0
        self.questions = ALL_QUESTIONS.copy()
        random.shuffle(self.questions)

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text='QUIZ PORTAL', font=('Orbitron', 32, 'bold'), fg='#5ffbf1', bg='#2d084f')
        self.title_label.pack(pady=(30, 0))
        # Subtitle
        self.subtitle_label = tk.Label(self.root, text='Master Chemistry, Physics & Mathematics', font=('Orbitron', 16), fg='#fff', bg='#2d084f')
        self.subtitle_label.pack(pady=(0, 20))
        # Progress bar
        self.progress_frame = tk.Frame(self.root, bg='#2d084f')
        self.progress_frame.pack(pady=(20, 0))
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.progress_frame, length=500, variable=self.progress_var, maximum=30, style='TProgressbar')
        self.progress.pack(side='left', padx=10)
        self.progress_label = tk.Label(self.progress_frame, text='', font=('Orbitron', 12), fg='#fff', bg='#2d084f')
        self.progress_label.pack(side='left')
        # Question frame
        self.q_frame = tk.Frame(self.root, bg='#3a2067', bd=3, relief='ridge', highlightbackground='#4e2a8e', highlightthickness=2)
        self.q_frame.pack(pady=30, padx=60, fill='x')
        self.question_label = tk.Label(self.q_frame, text='', font=('Orbitron', 22, 'bold'), fg='#fff', bg='#3a2067', wraplength=820, justify='left')
        self.question_label.pack(pady=(14, 10), anchor='w')
        # Options
        self.option_buttons = []
        self.selected_option = tk.IntVar(value=-1)
        for i in range(4):
            btn = tk.Radiobutton(
                self.q_frame, text='', variable=self.selected_option, value=i,
                font=('Segoe UI', 16), fg='#fff', bg='#3a2067',
                activebackground='#5ffbf1', activeforeground='#2d084f',
                selectcolor='#d16ba5', anchor='w', width=50, padx=14, pady=7,
                bd=0, highlightthickness=0, indicatoron=1
            )
            btn.pack(pady=7, anchor='w')
            self.option_buttons.append(btn)
        # Navigation
        self.nav_frame = tk.Frame(self.root, bg='#2d084f')
        self.nav_frame.pack(pady=12)
        self.prev_btn = tk.Button(
            self.nav_frame, text='← Previous', font=('Segoe UI', 14, 'bold'), state='disabled', command=self.prev_question,
            bg='#bdbdbd', fg='#fff', width=13, activebackground='#a0a0a0', activeforeground='#fff', bd=0, relief='flat',
            highlightthickness=0, padx=10, pady=8, cursor='hand2'
        )
        self.prev_btn.pack(side='left', padx=10)
        self.next_btn = tk.Button(
            self.nav_frame, text='Next →', font=('Segoe UI', 14, 'bold'), command=self.next_question,
            bg='#2d6cdf', fg='#fff', width=13, activebackground='#1a4fa3', activeforeground='#fff', bd=0, relief='flat',
            highlightthickness=0, padx=10, pady=8, cursor='hand2'
        )
        self.next_btn.pack(side='left', padx=10)
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TProgressbar', foreground='#d16ba5', background='#d16ba5', thickness=8)

    def show_question(self):
        self.progress_var.set(self.question_index + 1)
        self.progress_label.config(text=f'{self.question_index + 1}/30')
        q = self.questions[self.question_index]
        self.question_label.config(text=q['question'])
        for i, opt in enumerate(q['options']):
            self.option_buttons[i].config(text=opt)
        # Restore previous selection
        if self.selected_answers[self.question_index] is not None:
            self.selected_option.set(self.selected_answers[self.question_index])
        else:
            self.selected_option.set(-1)
        # Navigation button state
        self.prev_btn.config(state='normal' if self.question_index > 0 else 'disabled')
        if self.question_index == 29:
            self.next_btn.config(text='Submit', command=self.submit_quiz)
        else:
            self.next_btn.config(text='Next →', command=self.next_question)

    def prev_question(self):
        self.selected_answers[self.question_index] = self.selected_option.get() if self.selected_option.get() != -1 else None
        if self.question_index > 0:
            self.question_index -= 1
            self.show_question()

    def next_question(self):
        self.selected_answers[self.question_index] = self.selected_option.get() if self.selected_option.get() != -1 else None
        if self.selected_option.get() == -1:
            messagebox.showwarning('Select an option', 'Please select an option before proceeding.')
            return
        if self.question_index < 29:
            self.question_index += 1
            self.show_question()

    def submit_quiz(self):
        self.selected_answers[self.question_index] = self.selected_option.get() if self.selected_option.get() != -1 else None
        if self.selected_option.get() == -1:
            messagebox.showwarning('Select an option', 'Please select an option before submitting.')
            return
        correct = 0
        for idx, ans in enumerate(self.selected_answers):
            if ans == self.questions[idx]['answer']:
                correct += 1
        self.score = correct
        msg = f'You scored {correct}/30.'
        messagebox.showinfo('Quiz Result', msg)
        self.reset_quiz()
        self.show_question()

if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop() 