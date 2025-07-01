import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime
import ctypes
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# Enable DPI awareness for crisp UI on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

# In-memory database
expenses = []  # Each entry: {'category': ..., 'amount': ..., 'date': ...}

# --- Tab switching logic ---
def show_frame(frame):
    for f in content_frames.values():
        f.pack_forget()
    frame.pack(fill='both', expand=True)

# --- Dashboard View ---
def update_dashboard():
    total = sum(e['amount'] for e in expenses)
    count = len(expenses)
    dashboard_total_label.config(text=f"Total Expense: ₹{total:.2f}")
    dashboard_count_label.config(text=f"Number of Expenses: {count}")

def dashboard_view():
    update_dashboard()
    show_frame(content_frames['dashboard'])

# --- Add Expense View ---
def add_expense():
    category = category_var.get()
    amount_str = amount_entry.get()
    expense_date = date_picker.get_date()
    if not category or not amount_str:
        messagebox.showerror('Error', 'Please fill all fields.')
        return
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror('Error', 'Amount must be a number.')
        return
    entry = {'category': category, 'amount': amount, 'date': expense_date}
    expenses.append(entry)
    update_recent_expenses()
    update_total_label()
    amount_entry.delete(0, tk.END)
    category_var.set('')
    date_picker.set_date(date.today())

def update_recent_expenses():
    for widget in recent_frame.winfo_children():
        widget.destroy()
    if not expenses:
        tk.Label(recent_frame, text="No expenses added yet", fg="#999", bg="white",
                 font=("Segoe UI", 11, "italic")).pack(pady=30)
    else:
        for entry in reversed(expenses[-10:]):
            text = f"{entry['date'].strftime('%b %d, %Y')} | {entry['category']} | ₹{entry['amount']:.2f}"
            tk.Label(recent_frame, text=text, anchor='w', bg="white", fg="#333", font=("Segoe UI", 11)).pack(fill='x', pady=2)

def update_total_label():
    total = sum(e['amount'] for e in expenses)
    total_label.config(text=f"Total Expense: ₹{total:.2f}")

def add_expense_view():
    update_recent_expenses()
    update_total_label()
    show_frame(content_frames['add_expense'])

# --- Monthly Summary View ---
def update_monthly_summary():
    for widget in monthly_summary_frame.winfo_children():
        widget.destroy()
    if not expenses:
        tk.Label(monthly_summary_frame, text="No expenses to summarize", fg="#999", bg="white",
                 font=("Segoe UI", 11, "italic")).pack(pady=30)
        return
    # Group by month
    summary = {}
    for e in expenses:
        month = e['date'].strftime('%B %Y')
        if month not in summary:
            summary[month] = []
        summary[month].append(e)
    row = 0
    for month, items in sorted(summary.items()):
        month_total = sum(i['amount'] for i in items)
        tk.Label(monthly_summary_frame, text=f"{month}", font=("Segoe UI", 12, "bold"), bg="white").grid(row=row, column=0, sticky='w', pady=(10,0))
        tk.Label(monthly_summary_frame, text=f"Total: ₹{month_total:.2f}", font=("Segoe UI", 11, "bold"), bg="white", fg="#6a00ff").grid(row=row, column=1, sticky='w', padx=10, pady=(10,0))
        row += 1
        for i in items:
            tk.Label(monthly_summary_frame, text=f"  {i['date'].strftime('%b %d')} | {i['category']} | ₹{i['amount']:.2f}", bg="white", font=("Segoe UI", 10)).grid(row=row, column=0, columnspan=2, sticky='w', padx=10)
            row += 1

def monthly_summary_view():
    update_monthly_summary()
    show_frame(content_frames['monthly_summary'])

# --- Charts View ---
def update_charts():
    for widget in charts_frame.winfo_children():
        widget.destroy()
    if not HAS_MPL:
        tk.Label(charts_frame, text="matplotlib is not installed.", fg="#ef4444", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=30)
        return
    if not expenses:
        tk.Label(charts_frame, text="No data to display.", fg="#999", bg="white", font=("Segoe UI", 11, "italic")).pack(pady=30)
        return
    # Pie chart by category
    cat_totals = {}
    for e in expenses:
        cat_totals[e['category']] = cat_totals.get(e['category'], 0) + e['amount']
    fig, ax = plt.subplots(figsize=(3,3), dpi=100)
    ax.pie(cat_totals.values(), labels=cat_totals.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title('Expenses by Category')
    canvas = FigureCanvasTkAgg(fig, master=charts_frame)
    canvas.get_tk_widget().pack(pady=20)
    canvas.draw()
    plt.close(fig)

def charts_view():
    update_charts()
    show_frame(content_frames['charts'])

# --- Main window ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x550")
root.configure(bg="#f7f9fc")

# Improve font rendering and scaling
root.tk.call('tk', 'scaling', 1.0)  # Set scaling to 1.0 for crisp rendering

# Configure default fonts for better clarity
default_font = ("Segoe UI", 10)  # Use Segoe UI for better Windows rendering
title_font = ("Segoe UI", 24, "bold")
subtitle_font = ("Segoe UI", 12)
button_font = ("Segoe UI", 10, "bold")
label_font = ("Segoe UI", 10)

dark_mode = {'enabled': False}

# --- Dark mode toggle logic ---
def set_theme():
    if dark_mode['enabled']:
        bg = '#181825'
        fg = '#f3f3f3'
        accent = '#6a00ff'
        card = '#232336'
        entry_bg = '#232336'
        entry_fg = '#f3f3f3'
        btn_bg = '#33334d'
        btn_fg = '#f3f3f3'
        nav_bg = '#232336'
        nav_fg = '#f3f3f3'
    else:
        bg = '#f7f9fc'
        fg = '#222'
        accent = '#6a00ff'
        card = 'white'
        entry_bg = 'white'
        entry_fg = '#222'
        btn_bg = '#111827'
        btn_fg = 'white'
        nav_bg = '#e0e7ff'
        nav_fg = '#444'
    # Root
    root.configure(bg=bg)
    # Header
    title.config(bg=bg, fg=accent)
    subtitle.config(bg=bg, fg="#555" if not dark_mode['enabled'] else fg)
    # Nav
    nav_frame.config(bg=bg)
    for btn in nav_btns:
        btn.config(bg=nav_bg, fg=nav_fg)
    # Main frame
    main_frame.config(bg=bg)
    # Dashboard
    dashboard_frame.config(bg=card)
    dashboard_total_label.config(bg=card, fg="#ef4444" if not dark_mode['enabled'] else '#f87171')
    dashboard_count_label.config(bg=card, fg=fg)
    # Add Expense
    add_expense_outer.config(bg=bg)
    try:
        add_expense_frame.config(bg=card, fg=fg)
    except Exception:
        add_expense_frame.config(bg=card)
    for widget in add_expense_frame.winfo_children():
        try:
            if isinstance(widget, tk.Label):
                widget.config(bg=card, fg=fg)
            elif isinstance(widget, tk.Entry):
                widget.config(bg=entry_bg, fg=entry_fg)
            elif isinstance(widget, tk.Button):
                widget.config(bg=btn_bg, fg=btn_fg)
        except Exception:
            pass
    # Style for ttk.Combobox and DateEntry
    style = ttk.Style()
    if dark_mode['enabled']:
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
        style.configure('TEntry', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
        style.configure('DateEntry', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
    else:
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
        style.configure('TEntry', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
        style.configure('DateEntry', fieldbackground=entry_bg, background=entry_bg, foreground=entry_fg)
    recent_frame.config(bg=card)
    for widget in recent_frame.winfo_children():
        try:
            if isinstance(widget, tk.Label):
                widget.config(bg=card, fg=fg)
        except Exception:
            pass
    bottom_frame.config(bg=bg)
    total_label.config(bg=bg, fg="#ef4444" if not dark_mode['enabled'] else '#f87171')
    # Monthly Summary
    monthly_summary_outer.config(bg=bg)
    monthly_summary_frame.config(bg=card)
    for widget in monthly_summary_frame.winfo_children():
        try:
            if isinstance(widget, tk.Label):
                widget.config(bg=card, fg=fg)
        except Exception:
            pass
    # Charts
    charts_outer.config(bg=bg)
    charts_frame.config(bg=card)
    for widget in charts_frame.winfo_children():
        try:
            if isinstance(widget, tk.Label):
                widget.config(bg=card, fg=fg)
        except Exception:
            pass
    # Dark mode button
    dark_btn.config(bg=nav_bg, fg=nav_fg)

def toggle_dark_mode():
    dark_mode['enabled'] = not dark_mode['enabled']
    dark_btn.config(text='☀️ Light Mode' if dark_mode['enabled'] else '🌙 Dark Mode')
    set_theme()

# Header
title = tk.Label(root, text="💳 Expense Tracker", font=title_font, fg="#6a00ff", bg="#f7f9fc")
title.pack(pady=10, side='top')
# Dark mode button
dark_btn = tk.Button(root, text='🌙 Dark Mode', font=button_font, bg="#e0e7ff", fg="#444", relief='flat', command=toggle_dark_mode)
dark_btn.place(relx=1.0, x=-20, y=20, anchor='ne')

subtitle = tk.Label(root, text="Take control of your finances with our modern expense tracking solution.",
                    font=subtitle_font, fg="#555", bg="#f7f9fc")
subtitle.pack()

# Navigation tabs (functional)
nav_frame = tk.Frame(root, bg="#f7f9fc")
nav_frame.pack(pady=10)
nav_btns = []
for i, (tab, callback) in enumerate([
    ("📊 Dashboard", dashboard_view),
    ("📝 Add Expense", add_expense_view),
    ("📅 Monthly Summary", monthly_summary_view),
    ("📈 Charts", charts_view)
]):
    btn = tk.Button(nav_frame, text=tab, relief="flat", font=button_font,
                    fg="#444", bg="#e0e7ff", padx=15, pady=5, command=callback)
    btn.pack(side=tk.LEFT, padx=5)
    nav_btns.append(btn)

# Main content area (swappable frames)
main_frame = tk.Frame(root, bg="#f7f9fc")
main_frame.pack(pady=10, padx=20, fill="both", expand=True)

content_frames = {}

# Dashboard Frame
dashboard_frame = tk.Frame(main_frame, bg="white")
dashboard_total_label = tk.Label(dashboard_frame, text="Total Expense: ₹0.00", font=("Segoe UI", 16, "bold"), fg="#ef4444", bg="white")
dashboard_total_label.pack(pady=(40,10))
dashboard_count_label = tk.Label(dashboard_frame, text="Number of Expenses: 0", font=("Segoe UI", 13), fg="#333", bg="white")
dashboard_count_label.pack(pady=10)
content_frames['dashboard'] = dashboard_frame

# Add Expense Frame
add_expense_outer = tk.Frame(main_frame, bg="#f7f9fc")
add_expense_frame = tk.LabelFrame(add_expense_outer, text="➕ Add Expense", font=label_font,
                                  padx=20, pady=20, bg="white", fg="#111", labelanchor='n')
add_expense_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)
# Category Dropdown
tk.Label(add_expense_frame, text="Category", font=label_font, bg="white").pack(anchor='w')
global category_var
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(add_expense_frame, textvariable=category_var, state="readonly")
category_dropdown["values"] = ("Food", "Transport", "Bills", "Shopping", "Other")
category_dropdown.pack(fill="x", pady=5)
# Amount Entry
tk.Label(add_expense_frame, text="Amount (₹)", font=label_font, bg="white").pack(anchor='w')
global amount_entry
amount_entry = ttk.Entry(add_expense_frame)
amount_entry.pack(fill="x", pady=5)
# Date Picker
tk.Label(add_expense_frame, text="Date", font=label_font, bg="white").pack(anchor='w')
global date_picker
date_picker = DateEntry(add_expense_frame, width=20, background='darkblue', foreground='white', borderwidth=2)
date_picker.set_date(date.today())
date_picker.pack(fill="x", pady=5)
# Add Button
tk.Button(add_expense_frame, text="Add Expense", command=add_expense, bg="#111827", fg="white", font=button_font, relief="flat").pack(pady=10, fill='x')
# Right Pane - Recent Expenses
global recent_frame
recent_frame = tk.LabelFrame(add_expense_outer, text="🕓 Recent Expenses", font=("Segoe UI", 12, "bold"),
                             padx=20, pady=20, bg="white", fg="#111", labelanchor='n')
recent_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)
tk.Label(recent_frame, text="No expenses added yet", fg="#999", bg="white",
         font=("Segoe UI", 11, "italic")).pack(pady=30)
# Total Expense Label
bottom_frame = tk.Frame(add_expense_outer, bg="#f7f9fc")
bottom_frame.pack(fill='x', pady=(0, 10))
global total_label
total_label = tk.Label(bottom_frame, text="Total Expense: ₹0.00", font=("Segoe UI", 13, "bold"), fg="#ef4444", bg="#f7f9fc")
total_label.pack(side='left', padx=(40, 0))
content_frames['add_expense'] = add_expense_outer

# Monthly Summary Frame
global monthly_summary_frame
monthly_summary_outer = tk.Frame(main_frame, bg="#f7f9fc")
monthly_summary_frame = tk.Frame(monthly_summary_outer, bg="white")
monthly_summary_frame.pack(fill='both', expand=True, padx=20, pady=20)
content_frames['monthly_summary'] = monthly_summary_outer

# Charts Frame
global charts_frame
charts_outer = tk.Frame(main_frame, bg="#f7f9fc")
charts_frame = tk.Frame(charts_outer, bg="white")
charts_frame.pack(fill='both', expand=True, padx=20, pady=20)
content_frames['charts'] = charts_outer

# Start with Dashboard
dashboard_view()

set_theme()

root.mainloop()
