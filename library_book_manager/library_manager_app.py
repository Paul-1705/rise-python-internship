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

# Modern color palette
BG_COLOR = '#232b32'
SIDEBAR_COLOR = '#1a2127'
SIDEBAR_BORDER = '#2e3942'
MAIN_BG = '#27313a'
CARD_COLOR = '#2e3942'
CARD_SHADOW = '#1a2127'
ACCENT_COLOR = '#f6c343'
ACCENT_HOVER = '#ffe082'
TEXT_COLOR = '#f5f6fa'
PLACEHOLDER_COLOR = '#b0b6be'
DELETE_COLOR = '#ff5c5c'
DELETE_HOVER = '#ffb3b3'

# Improved fonts with better rendering
FONT = ('Microsoft YaHei UI', 11)  # Better for Windows
TITLE_FONT = ('Microsoft YaHei UI', 18, 'bold')
SECTION_FONT = ('Microsoft YaHei UI', 13, 'bold')

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind('<Enter>', self.show)
        widget.bind('<Leave>', self.hide)
    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox('insert') if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 40
        y = y + self.widget.winfo_rooty() + cy + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f'+{x}+{y}')
        label = tk.Label(tw, text=self.text, justify='left', bg='#333', fg='white', relief='solid', borderwidth=1, font=('Microsoft YaHei UI', 9))
        label.pack(ipadx=8, ipady=3)
    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class LibraryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Library Book Manager')
        self.root.geometry('1100x650')
        self.root.configure(bg=BG_COLOR)
        
        # Configure window for better rendering
        self.root.tk.call('tk', 'scaling', 1.0)
        self.root.option_add('*Font', FONT)
        
        self.books = []
        self.setup_sidebar()
        self.setup_topbar()
        self.setup_main_area()

    def setup_sidebar(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=70, highlightbackground=SIDEBAR_BORDER, highlightthickness=1)
        sidebar.pack(side='left', fill='y')
        icons = [
            ('🏠', 'Home'),
            ('📚', 'Books'),
            ('👤', 'Profile'),
            ('⭐', 'Favorites')
        ]
        for i, (icon, name) in enumerate(icons):
            btn = tk.Label(sidebar, text=icon, bg=SIDEBAR_COLOR, fg=ACCENT_COLOR,
                          font=('Segoe UI Emoji', 20), width=3, height=2, cursor='hand2')
            btn.pack(pady=12, padx=0)
            btn.bind('<Button-1>', lambda e, n=name: self.sidebar_action(n))
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=BG_COLOR))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=SIDEBAR_COLOR))
            Tooltip(btn, f'{name}')

    def setup_topbar(self):
        topbar = tk.Frame(self.root, bg=BG_COLOR, height=60, highlightbackground=SIDEBAR_BORDER, highlightthickness=1)
        topbar.pack(side='top', fill='x')
        title = tk.Label(topbar, text='Library', bg=BG_COLOR, fg=ACCENT_COLOR, font=TITLE_FONT)
        title.pack(side='left', padx=28)
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(topbar, bg=BG_COLOR)
        search_frame.pack(side='left', padx=20)
        search_icon = tk.Label(search_frame, text='🔍', bg=CARD_COLOR, fg=ACCENT_COLOR, font=('Segoe UI Emoji', 12))
        search_icon.pack(side='left', padx=(0,0))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=FONT, width=28, bg=CARD_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=0, relief='flat', highlightthickness=0)
        search_entry.pack(side='left', padx=(0,0), ipady=6)
        search_btn = tk.Button(search_frame, text='Search', command=self.search_books, bg=ACCENT_COLOR, fg=BG_COLOR, font=('Microsoft YaHei UI', 10, 'bold'), bd=0, relief='flat', cursor='hand2', activebackground=ACCENT_HOVER)
        search_btn.pack(side='left', padx=(8,0))
        Tooltip(search_btn, 'Search books by title')
        avatar = tk.Canvas(topbar, width=38, height=38, bg=BG_COLOR, highlightthickness=0)
        avatar.create_oval(4, 4, 34, 34, fill=ACCENT_COLOR, outline='')
        avatar.create_text(19, 19, text='A', font=('Microsoft YaHei UI', 14, 'bold'), fill=BG_COLOR)
        avatar.pack(side='right', padx=24)
        Tooltip(avatar, 'Admin Profile')

    def setup_main_area(self):
        main = tk.Frame(self.root, bg=MAIN_BG)
        main.pack(fill='both', expand=True, padx=0, pady=(0,0))
        # Add Book section
        add_frame = tk.Frame(main, bg=CARD_COLOR, bd=0, highlightbackground=SIDEBAR_BORDER, highlightthickness=1)
        add_frame.pack(fill='x', pady=18, padx=30, ipady=8)
        tk.Label(add_frame, text='Add Book', bg=CARD_COLOR, fg=ACCENT_COLOR, font=SECTION_FONT).pack(side='left', padx=(0,20))
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.title_entry = tk.Entry(add_frame, textvariable=self.title_var, width=18, font=FONT, bg=MAIN_BG, fg=PLACEHOLDER_COLOR, insertbackground=TEXT_COLOR, bd=0, relief='flat', highlightthickness=0)
        self.title_entry.pack(side='left', padx=5, ipady=5)
        self.set_placeholder(self.title_entry, self.title_var, 'Name')
        self.author_entry = tk.Entry(add_frame, textvariable=self.author_var, width=14, font=FONT, bg=MAIN_BG, fg=PLACEHOLDER_COLOR, insertbackground=TEXT_COLOR, bd=0, relief='flat', highlightthickness=0)
        self.author_entry.pack(side='left', padx=5, ipady=5)
        self.set_placeholder(self.author_entry, self.author_var, 'Author')
        self.id_entry = tk.Entry(add_frame, textvariable=self.id_var, width=8, font=FONT, bg=MAIN_BG, fg=PLACEHOLDER_COLOR, insertbackground=TEXT_COLOR, bd=0, relief='flat', highlightthickness=0)
        self.id_entry.pack(side='left', padx=5, ipady=5)
        self.set_placeholder(self.id_entry, self.id_var, 'ID')
        add_btn = tk.Button(add_frame, text='Add', command=self.add_book, bg=ACCENT_COLOR, fg=BG_COLOR, font=('Microsoft YaHei UI', 11, 'bold'), bd=0, relief='flat', cursor='hand2', activebackground=ACCENT_HOVER)
        add_btn.pack(side='left', padx=14)
        Tooltip(add_btn, 'Add a new book')
        # Book list area
        self.books_frame = tk.Frame(main, bg=MAIN_BG)
        self.books_frame.pack(fill='both', expand=True, pady=10, padx=20)
        self.refresh_books()

    def set_placeholder(self, entry, var, placeholder):
        def on_focus_in(event):
            if var.get() == placeholder:
                entry.delete(0, 'end')
                entry.config(fg=TEXT_COLOR)
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=PLACEHOLDER_COLOR)
        entry.insert(0, placeholder)
        entry.config(fg=PLACEHOLDER_COLOR)
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def add_book(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        book_id = self.id_var.get().strip()
        if title == 'Name': title = ''
        if author == 'Author': author = ''
        if book_id == 'ID': book_id = ''
        if not title or not author or not book_id:
            messagebox.showwarning('Input Error', 'Please fill all fields.')
            return
        if any(b['id'] == book_id for b in self.books):
            messagebox.showerror('Duplicate ID', 'A book with this ID already exists.')
            return
        self.books.append({'id': book_id, 'title': title, 'author': author})
        self.title_var.set('')
        self.author_var.set('')
        self.id_var.set('')
        self.set_placeholder(self.title_entry, self.title_var, 'Name')
        self.set_placeholder(self.author_entry, self.author_var, 'Author')
        self.set_placeholder(self.id_entry, self.id_var, 'ID')
        self.refresh_books()

    def search_books(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.refresh_books()
            return
        filtered = [b for b in self.books if query in b['title'].lower()]
        self.refresh_books(filtered)

    def delete_book(self, book_id):
        self.books = [b for b in self.books if b['id'] != book_id]
        self.refresh_books()

    def refresh_books(self, books=None):
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        books = books if books is not None else self.books
        if not books:
            tk.Label(self.books_frame, text='No books to display.', bg=MAIN_BG, fg=TEXT_COLOR, font=FONT).pack(pady=30)
            return
        for i, book in enumerate(books):
            card_outer = tk.Frame(self.books_frame, bg=CARD_SHADOW, bd=0)
            card_outer.grid(row=i//4, column=i%4, padx=18, pady=18, sticky='nsew')
            card = tk.Frame(card_outer, bg=CARD_COLOR, bd=0, relief='flat', highlightbackground=SIDEBAR_BORDER, highlightthickness=1)
            card.pack(padx=2, pady=2)
            card.config(cursor='hand2')
            card.bind('<Enter>', lambda e, c=card: c.config(bg=ACCENT_HOVER))
            card.bind('<Leave>', lambda e, c=card: c.config(bg=CARD_COLOR))
            # Book cover placeholder
            cover = tk.Canvas(card, width=60, height=80, bg=ACCENT_COLOR, bd=0, highlightthickness=0)
            cover.create_text(30, 40, text='📖', font=('Segoe UI Emoji', 24))
            cover.pack(pady=(10,0))
            # Book info
            tk.Label(card, text=book['title'], bg=CARD_COLOR, fg=TEXT_COLOR, font=('Microsoft YaHei UI', 11, 'bold')).pack(pady=(8,0))
            tk.Label(card, text=f"by {book['author']}", bg=CARD_COLOR, fg=PLACEHOLDER_COLOR, font=('Microsoft YaHei UI', 9)).pack()
            tk.Label(card, text=f"ID: {book['id']}", bg=CARD_COLOR, fg=PLACEHOLDER_COLOR, font=('Microsoft YaHei UI', 8)).pack()
            # Delete button
            del_btn = tk.Button(card, text='🗑', command=lambda bid=book['id']: self.delete_book(bid),
                      bg=DELETE_COLOR, fg='white', font=('Segoe UI Emoji', 10), bd=0, relief='flat', cursor='hand2', activebackground=DELETE_HOVER)
            del_btn.pack(pady=8)
            Tooltip(del_btn, 'Delete this book')

    def sidebar_action(self, name):
        win = tk.Toplevel(self.root)
        win.title(f'{name} Instructions')
        win.geometry('500x400')
        win.configure(bg=MAIN_BG)
        tk.Label(win, text=f'{name} Section', bg=MAIN_BG, fg=ACCENT_COLOR, font=('Microsoft YaHei UI', 16, 'bold')).pack(pady=(18,8))
        frame = tk.Frame(win, bg=MAIN_BG)
        frame.pack(fill='both', expand=True, padx=18, pady=10)
        text = tk.Text(frame, wrap='word', bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT, bd=0, relief='flat')
        text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        instructions = self.get_instructions_for_section(name)
        text.insert('1.0', instructions)
        text.config(state='disabled')

    def get_instructions_for_section(self, name):
        if name == 'Home':
            return (
                'Welcome to the Library Manager Home section!\n\n'
                'Here you can get an overview of your library, see recent activity, and access quick links to other sections.\n\n'
                'Use the sidebar to navigate to Books, Profile, or Favorites.'
            )
        elif name == 'Books':
            return (
                'Books Section Instructions:\n\n'
                '- Add new books using the form on the main page.\n'
                '- Search for books by title using the search bar.\n'
                '- Delete books by clicking the Delete button on a book card.\n'
                '- All your books are displayed as cards in the main area.'
            )
        elif name == 'Profile':
            return (
                'Profile Section Instructions:\n\n'
                '- View and edit your user information.\n'
                '- Track your reading history and preferences.\n'
                '- Customize your experience in the app.'
            )
        elif name == 'Favorites':
            return (
                'Favorites Section Instructions:\n\n'
                '- View your favorite books.\n'
                '- Add or remove books from your favorites list.\n'
                '- Quickly access your most loved titles.'
            )
        else:
            return 'Instructions for this section are not available.'

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryManagerApp(root)
    root.mainloop() 