import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

# Enable DPI awareness for Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

# Mock exchange rates relative to USD
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'JPY': 155.3,
    'AUD': 1.51,
    'CAD': 1.36,
    'CHF': 0.90,
    'CNY': 7.24,
    'INR': 83.4,
    'BRL': 5.13
}
CURRENCY_INFO = {
    'USD': {'symbol': '$', 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'name': 'Euro'},
    'GBP': {'symbol': '£', 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen'},
    'AUD': {'symbol': 'A$', 'name': 'Australian Dollar'},
    'CAD': {'symbol': 'C$', 'name': 'Canadian Dollar'},
    'CHF': {'symbol': 'CHF', 'name': 'Swiss Franc'},
    'CNY': {'symbol': '¥', 'name': 'Chinese Yuan'},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee'},
    'BRL': {'symbol': 'R$', 'name': 'Brazilian Real'},
}
CURRENCIES = list(EXCHANGE_RATES.keys())

class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind('<Configure>', self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete('gradient')
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            self.create_line(0, i, width, i, tags=('gradient',), fill=color)
        self.lower('gradient')

class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Currency Converter')
        self.configure(bg='#ede7f6')
        self.geometry('700x750')
        self.resizable(False, False)
        self.option_add('*Font', 'Arial 11')
        self.create_widgets()

    def create_widgets(self):
        # Card Frame
        card = tk.Frame(self, bg='#fff', bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='c', width=600, height=670)
        card.grid_propagate(False)
        card.update()
        card.after(10, lambda: card.config(bg='#fff'))
        card.config(highlightbackground='#d1e3fa', highlightcolor='#d1e3fa', highlightthickness=2)
        card.pack_propagate(False)

        # Gradient Header
        header = GradientFrame(card, '#4f8cff', '#a259e6', height=80, width=600, bd=0, highlightthickness=0)
        header.pack(fill='x', side='top')
        header.create_text(300, 40, text='\u2191 Convert Currency', font=('Arial', 22, 'bold'), fill='white')

        # Subtitle
        subtitle = tk.Label(card, text='Convert between major currencies instantly', bg='#fff', fg='#7a7a7a', font=('Arial', 11))
        subtitle.pack(pady=(10, 0))

        # Amount
        amount_label = tk.Label(card, text='Amount', bg='#fff', fg='#222', font=('Arial', 11, 'bold'))
        amount_label.pack(anchor='w', padx=32, pady=(18, 0))
        self.amount_entry = tk.Entry(card, font=('Arial', 13), bd=1, relief='solid', highlightthickness=0, width=28, justify='left')
        self.amount_entry.pack(padx=32, pady=6)

        # From/To Frame
        ft_frame = tk.Frame(card, bg='#fff')
        ft_frame.pack(pady=(10, 0))

        # From
        from_label = tk.Label(ft_frame, text='From', bg='#fff', fg='#222', font=('Arial', 10, 'bold'))
        from_label.grid(row=0, column=0, sticky='w', padx=(0, 0))
        to_label = tk.Label(ft_frame, text='To', bg='#fff', fg='#222', font=('Arial', 10, 'bold'))
        to_label.grid(row=0, column=2, sticky='w', padx=(30, 0))

        self.from_currency = ttk.Combobox(ft_frame, values=[f"{CURRENCY_INFO[c]['symbol']} {c} - {CURRENCY_INFO[c]['name']}" for c in CURRENCIES], state='readonly', width=22, font=('Arial', 11))
        self.from_currency.set(f"$ USD - US Dollar")
        self.from_currency.grid(row=1, column=0, padx=(0, 10), pady=4)

        self.to_currency = ttk.Combobox(ft_frame, values=[f"{CURRENCY_INFO[c]['symbol']} {c} - {CURRENCY_INFO[c]['name']}" for c in CURRENCIES], state='readonly', width=22, font=('Arial', 11))
        self.to_currency.set(f"₹ INR - Indian Rupee")
        self.to_currency.grid(row=1, column=2, padx=(30, 0), pady=4)

        # Swap Button
        swap_btn = tk.Button(ft_frame, text='⟲', font=('Arial', 13, 'bold'), bg='#f0f4f8', fg='#4f8cff', bd=0, relief='flat', command=self.swap_currencies, cursor='hand2', activebackground='#eaf1fb', activeforeground='#a259e6')
        swap_btn.grid(row=1, column=1, padx=2)

        # Convert Button
        self.convert_btn = tk.Canvas(card, width=340, height=44, bd=0, highlightthickness=0)
        self.convert_btn.pack(pady=22)
        self._draw_gradient_button(self.convert_btn, '#4f8cff', '#a259e6')
        self.convert_btn.create_text(170, 22, text='Convert', font=('Arial', 14, 'bold'), fill='white', tags='btn_text')
        self.convert_btn.tag_bind('btn_text', '<Button-1>', lambda e: self.convert_currency())
        self.convert_btn.bind('<Button-1>', lambda e: self.convert_currency())

        # Result Card
        self.result_card = tk.Frame(card, bg='#eafcf3', highlightbackground='#b6e7d6', highlightcolor='#b6e7d6', highlightthickness=1)
        self.result_card.pack(pady=(10, 0), padx=20, fill='x')
        self.result_label = tk.Label(self.result_card, text='', font=('Arial', 15, 'bold'), bg='#eafcf3', fg='#222')
        self.result_label.pack(padx=10, pady=12)
        self.result_title = tk.Label(self.result_card, text='Conversion Result', font=('Arial', 11), bg='#eafcf3', fg='#6bbf8e')
        self.result_title.pack(side='top', anchor='w', padx=10, pady=(4, 0))
        self.result_card.pack_forget()

    def _draw_gradient_button(self, canvas, color1, color2):
        width = int(canvas['width'])
        height = int(canvas['height'])
        (r1, g1, b1) = self.winfo_rgb(color1)
        (r2, g2, b2) = self.winfo_rgb(color2)
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height
        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            canvas.create_line(0, i, width, i, fill=color)
        canvas.create_rectangle(0, 0, width, height, outline='#4f8cff', width=1)

    def swap_currencies(self):
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)

    def convert_currency(self):
        from_cur = self.from_currency.get().split()[1]
        to_cur = self.to_currency.get().split()[1]
        amount_str = self.amount_entry.get()
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid Input', 'Please enter a valid positive number for amount.')
            return
        if from_cur == to_cur:
            result = amount
        else:
            usd_amount = amount / EXCHANGE_RATES[from_cur]
            result = usd_amount * EXCHANGE_RATES[to_cur]
        from_symbol = CURRENCY_INFO[from_cur]['symbol']
        to_symbol = CURRENCY_INFO[to_cur]['symbol']
        self.result_label.config(text=f'{from_symbol}{amount:.2f} = {to_symbol}{result:.2f}')
        self.result_card.pack(pady=(10, 0), padx=20, fill='x')
        self.result_title.lift()

if __name__ == '__main__':
    app = CurrencyConverterApp()
    app.mainloop() 