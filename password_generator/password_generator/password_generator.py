import tkinter as tk
from tkinter import ttk
import random
import string

# Password generation logic
def generate_password(length, use_numbers, use_special):
    chars = string.ascii_letters
    if use_numbers:
        chars += string.digits
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?/'
    if not chars:
        return ''
    return ''.join(random.choice(chars) for _ in range(length))

# Main App
class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('StrongPass Generator')
        self.configure(bg='#f6f8ff')
        self.geometry('420x480')
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Card Frame
        card = tk.Frame(self, bg='white', bd=0, relief='flat')
        card.place(relx=0.5, rely=0.5, anchor='center', width=380, height=440)

        # Shield Icon
        icon_label = tk.Label(card, text='🛡️', font=('Segoe UI Emoji', 38), bg='white')
        icon_label.pack(pady=(24, 0))

        # Title
        title = tk.Label(card, text='StrongPass Generator', font=('Segoe UI Semibold', 20), fg='#7b3ff2', bg='white')
        title.pack(pady=(10, 0))

        # Subtitle
        subtitle = tk.Label(card, text='Generate secure, customizable passwords instantly', font=('Segoe UI', 11), fg='#6b6b6b', bg='white')
        subtitle.pack(pady=(2, 18))

        # Password Length
        self.length_var = tk.IntVar(value=12)
        length_frame = tk.Frame(card, bg='white')
        length_frame.pack(fill='x', padx=28)
        tk.Label(length_frame, text='Password Length: ', font=('Segoe UI Semibold', 11), bg='white').pack(side='left')
        self.length_value = tk.Label(length_frame, text=str(self.length_var.get()), font=('Segoe UI Semibold', 11), bg='white')
        self.length_value.pack(side='left')

        # Slider
        slider = ttk.Scale(card, from_=4, to=50, orient='horizontal', variable=self.length_var, command=self._update_length, style='TScale')
        slider.pack(fill='x', padx=28, pady=(0, 0))
        minmax_frame = tk.Frame(card, bg='white')
        minmax_frame.pack(fill='x', padx=28)
        tk.Label(minmax_frame, text='4', font=('Segoe UI', 9), bg='white', fg='#888').pack(side='left')
        tk.Label(minmax_frame, text='50', font=('Segoe UI', 9), bg='white', fg='#888').pack(side='right')

        # Checkboxes
        self.numbers_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        check1 = ttk.Checkbutton(card, text='Include Numbers (0-9)', variable=self.numbers_var, style='TCheckbutton')
        check2 = ttk.Checkbutton(card, text='Include Special Characters (!@#$%...)', variable=self.special_var, style='TCheckbutton')
        check1.pack(anchor='w', padx=28, pady=(18, 0))
        check2.pack(anchor='w', padx=28, pady=(6, 0))

        # Password Display
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(card, textvariable=self.password_var, font=('Consolas', 13), justify='center', state='readonly')
        password_entry.pack(fill='x', padx=28, pady=(18, 0))

        # Generate Button
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TButton', font=('Segoe UI Semibold', 13), padding=8)
        style.map('TButton', background=[('active', '#7b3ff2')], foreground=[('active', 'white')])
        self._set_gradient_button_style(style)
        gen_btn = ttk.Button(card, text='  🛡️  Generate Password  ', style='Gradient.TButton', command=self._on_generate)
        gen_btn.pack(fill='x', padx=28, pady=(24, 0))

    def _set_gradient_button_style(self, style):
        # Tkinter doesn't support gradient natively, so use a solid color close to the image
        style.configure('Gradient.TButton', background='#7b3ff2', foreground='white', borderwidth=0, focusthickness=3, focuscolor='none')

    def _update_length(self, event):
        self.length_value.config(text=str(self.length_var.get()))

    def _on_generate(self):
        length = self.length_var.get()
        use_numbers = self.numbers_var.get()
        use_special = self.special_var.get()
        password = generate_password(length, use_numbers, use_special)
        self.password_var.set(password)

if __name__ == '__main__':
    app = PasswordGeneratorApp()
    app.mainloop() 