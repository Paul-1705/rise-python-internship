import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.configure(bg="#192231")
        self.tasks = []

        # Fonts and colors
        self.bg_color = "#192231"
        self.panel_color = "#232e42"
        self.accent_color = "#00bcd4"
        self.button_color = "#00bcd4"
        self.button_fg = "#fff"
        self.text_color = "#fff"
        self.completed_color = "#90a4ae"  # Light gray for completed
        self.completed_check = "\u2713"  # Unicode checkmark
        self.font_title = ("Segoe UI", 24, "bold")
        self.font_subtitle = ("Segoe UI", 12)
        self.font_label = ("Segoe UI", 10, "bold")
        self.font_normal = ("Segoe UI", 10)
        self.font_completed = ("Segoe UI", 10, "bold")

        # Header
        self.header = tk.Frame(self.root, bg=self.bg_color)
        self.header.pack(fill=tk.X, pady=(20, 10))
        tk.Label(self.header, text="⚡ TaskMaster ", fg="#1de9b6", bg=self.bg_color, font=("Segoe UI", 28, "bold"), anchor="w").pack(side=tk.LEFT)
        tk.Label(self.header, text="Pro", fg="#fff", bg=self.bg_color, font=("Segoe UI", 28, "bold"), anchor="w").pack(side=tk.LEFT)
        tk.Label(self.header, text="\nYour powerful task management companion", fg="#b0bec5", bg=self.bg_color, font=self.font_subtitle, anchor="w").pack(anchor="w", padx=(5,0))

        # Stats
        self.stats = tk.Frame(self.root, bg=self.bg_color)
        self.stats.pack(fill=tk.X, pady=(0, 10))
        self.total_var = tk.StringVar(value="0")
        self.completed_var = tk.StringVar(value="0")
        self.remaining_var = tk.StringVar(value="0")
        for i, (label, var, color) in enumerate([
            ("Total Tasks", self.total_var, "#00e676"),
            ("Completed", self.completed_var, "#00bcd4"),
            ("Remaining", self.remaining_var, "#ffd600")]):
            stat = tk.Frame(self.stats, bg=self.bg_color)
            stat.pack(side=tk.LEFT, padx=30)
            tk.Label(stat, textvariable=var, fg=color, bg=self.bg_color, font=("Segoe UI", 18, "bold")).pack()
            tk.Label(stat, text=label, fg="#b0bec5", bg=self.bg_color, font=self.font_label).pack()

        # Main panels
        self.main = tk.Frame(self.root, bg=self.bg_color)
        self.main.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Left: Add Task
        self.left_panel = tk.Frame(self.main, bg=self.panel_color, bd=0, relief=tk.RIDGE)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), pady=10)
        tk.Label(self.left_panel, text="+ Add New Task", fg=self.accent_color, bg=self.panel_color, font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(15, 10), padx=20)

        tk.Label(self.left_panel, text="Task Description", fg=self.text_color, bg=self.panel_color, font=self.font_label).pack(anchor="w", padx=20)
        self.entry = tk.Entry(self.left_panel, width=28, font=self.font_normal, bg="#263143", fg=self.text_color, insertbackground=self.text_color, relief=tk.FLAT)
        self.entry.pack(padx=20, pady=(0, 10))
        self.entry.bind('<Return>', lambda event: self.add_task())

        tk.Label(self.left_panel, text="Priority Level", fg=self.text_color, bg=self.panel_color, font=self.font_label).pack(anchor="w", padx=20)
        self.priority_var = tk.StringVar(value="Medium Priority")
        self.priority_menu = ttk.Combobox(self.left_panel, textvariable=self.priority_var, state="readonly", width=25, font=self.font_normal)
        self.priority_menu['values'] = ("High Priority", "Medium Priority", "Low Priority")
        self.priority_menu.pack(padx=20, pady=(0, 10))

        tk.Label(self.left_panel, text="Due Date (Optional)", fg=self.text_color, bg=self.panel_color, font=self.font_label).pack(anchor="w", padx=20)
        self.due_entry = tk.Entry(self.left_panel, width=28, font=self.font_normal, bg="#263143", fg=self.text_color, insertbackground=self.text_color, relief=tk.FLAT)
        self.due_entry.insert(0, "mm/dd/yyyy")
        self.due_entry.pack(padx=20, pady=(0, 15))

        self.add_button = tk.Button(self.left_panel, text="+ Add Task", command=self.add_task, bg=self.button_color, fg=self.button_fg, font=self.font_label, relief=tk.FLAT, activebackground="#0097a7", activeforeground="#fff")
        self.add_button.pack(padx=20, pady=(0, 20), fill=tk.X)

        # Right: Task List
        self.right_panel = tk.Frame(self.main, bg=self.panel_color, bd=0, relief=tk.RIDGE)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        top_right = tk.Frame(self.right_panel, bg=self.panel_color)
        top_right.pack(fill=tk.X, pady=(15, 0), padx=20)
        tk.Label(top_right, text="Your Tasks", fg=self.accent_color, bg=self.panel_color, font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        self.task_count_label = tk.Label(top_right, text="0", fg="#b0bec5", bg=self.panel_color, font=self.font_label)
        self.task_count_label.pack(side=tk.LEFT, padx=(5, 0))

        # Filters and sort
        filter_sort = tk.Frame(self.right_panel, bg=self.panel_color)
        filter_sort.pack(fill=tk.X, padx=20, pady=(5, 0))
        tk.Label(filter_sort, text=" ", bg=self.panel_color).pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="All Tasks")
        self.filter_menu = ttk.Combobox(filter_sort, textvariable=self.filter_var, state="readonly", width=12, font=self.font_normal)
        self.filter_menu['values'] = ("All Tasks", "Completed", "Remaining")
        self.filter_menu.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_menu.bind('<<ComboboxSelected>>', lambda e: self.update_task_view())
        self.sort_var = tk.StringVar(value="Date Created")
        self.sort_menu = ttk.Combobox(filter_sort, textvariable=self.sort_var, state="readonly", width=15, font=self.font_normal)
        self.sort_menu['values'] = ("Date Created", "Priority", "Due Date")
        self.sort_menu.pack(side=tk.LEFT)
        self.sort_menu.bind('<<ComboboxSelected>>', lambda e: self.update_task_view())

        # Text widget for tasks
        self.task_text = tk.Text(self.right_panel, width=50, height=12, font=self.font_normal, bg="#263143", fg=self.text_color, relief=tk.FLAT, wrap=tk.NONE, cursor="arrow")
        self.task_text.pack(padx=20, pady=(10, 0), fill=tk.BOTH, expand=True)
        self.task_text.config(state=tk.DISABLED)
        self.task_text.tag_configure("completed", foreground=self.completed_color, font=self.font_completed)
        self.task_text.tag_configure("checkmark", foreground="#00e676", font=self.font_completed)
        self.task_text.tag_configure("normal", foreground=self.text_color, font=self.font_normal)

        # No tasks label
        self.no_tasks_label = tk.Label(self.right_panel, text="No tasks found\nAdd your first task to get started!", fg="#b0bec5", bg=self.panel_color, font=self.font_normal, justify=tk.CENTER)
        self.no_tasks_label.pack(padx=20, pady=20)

        # Task actions
        actions = tk.Frame(self.right_panel, bg=self.panel_color)
        actions.pack(padx=20, pady=(0, 20), fill=tk.X)
        self.done_button = tk.Button(actions, text="Mark as Done", command=self.mark_done, bg=self.button_color, fg=self.button_fg, font=self.font_label, relief=tk.FLAT, activebackground="#0097a7", activeforeground="#fff")
        self.done_button.pack(side=tk.LEFT, padx=(0, 10))
        self.delete_button = tk.Button(actions, text="Delete Task", command=self.delete_task, bg="#e53935", fg="#fff", font=self.font_label, relief=tk.FLAT, activebackground="#b71c1c", activeforeground="#fff")
        self.delete_button.pack(side=tk.LEFT)

        # For selection
        self.selected_index = None
        self.task_text.bind("<Button-1>", self.on_text_click)

        self.update_task_view()

    def add_task(self):
        task = self.entry.get().strip()
        priority = self.priority_var.get()
        due = self.due_entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Please enter a task.")
            return
        due_date = None
        if due and due != "mm/dd/yyyy":
            try:
                due_date = datetime.strptime(due, "%m/%d/%Y")
            except ValueError:
                messagebox.showwarning("Date Error", "Please enter the due date in mm/dd/yyyy format.")
                return
        self.tasks.append({
            'task': task,
            'done': False,
            'priority': priority,
            'due': due_date,
            'created': datetime.now()
        })
        self.entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, "mm/dd/yyyy")
        self.priority_var.set("Medium Priority")
        self.update_task_view()

    def mark_done(self):
        if self.selected_index is not None:
            idx = self.get_actual_index(self.selected_index)
            self.tasks[idx]['done'] = not self.tasks[idx]['done']
            self.update_task_view()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def delete_task(self):
        if self.selected_index is not None:
            idx = self.get_actual_index(self.selected_index)
            del self.tasks[idx]
            self.selected_index = None
            self.update_task_view()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def get_actual_index(self, view_index):
        filtered = self.get_filtered_sorted_tasks(with_indices=True)
        return filtered[view_index][0]

    def get_filtered_sorted_tasks(self, with_indices=False):
        filtered = []
        for i, t in enumerate(self.tasks):
            if self.filter_var.get() == "Completed" and not t['done']:
                continue
            if self.filter_var.get() == "Remaining" and t['done']:
                continue
            filtered.append((i, t) if with_indices else t)
        sort_key = self.sort_var.get()
        if sort_key == "Priority":
            order = {"High Priority": 0, "Medium Priority": 1, "Low Priority": 2}
            filtered.sort(key=lambda x: order[(x[1] if with_indices else x)['priority']])
        elif sort_key == "Due Date":
            filtered.sort(key=lambda x: (x[1] if with_indices else x)['due'] or datetime.max)
        elif sort_key == "Date Created":
            filtered.sort(key=lambda x: (x[1] if with_indices else x)['created'])
        return filtered

    def update_task_view(self):
        filtered = self.get_filtered_sorted_tasks()
        self.task_text.config(state=tk.NORMAL)
        self.task_text.delete(1.0, tk.END)
        self.selected_index = None
        if not filtered:
            self.no_tasks_label.lift()
        else:
            self.no_tasks_label.lower()
        for idx, t in enumerate(filtered):
            start = self.task_text.index(tk.END)
            if t['done']:
                self.task_text.insert(tk.END, f" {self.completed_check} ", ("checkmark",))
                self.task_text.insert(tk.END, t['task'], ("completed",))
            else:
                self.task_text.insert(tk.END, "   ", ("normal",))
                self.task_text.insert(tk.END, t['task'], ("normal",))
            self.task_text.insert(tk.END, f" | {t['priority']}", ("normal",))
            if t['due']:
                self.task_text.insert(tk.END, f" | Due: {t['due'].strftime('%m/%d/%Y')}", ("normal",))
            self.task_text.insert(tk.END, "\n", ("normal",))
        self.task_text.config(state=tk.DISABLED)
        # Update stats
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['done'])
        remaining = total - completed
        self.total_var.set(str(total))
        self.completed_var.set(str(completed))
        self.remaining_var.set(str(remaining))
        self.task_count_label.config(text=f"{len(filtered)}")

    def on_text_click(self, event):
        # Select a line (task) by clicking
        index = self.task_text.index(f"@{event.x},{event.y}")
        line = int(index.split('.')[0]) - 1
        filtered = self.get_filtered_sorted_tasks()
        if 0 <= line < len(filtered):
            self.selected_index = line
            # Highlight the selected line
            self.task_text.config(state=tk.NORMAL)
            self.task_text.tag_remove("sel", "1.0", tk.END)
            self.task_text.tag_add("sel", f"{line+1}.0", f"{line+1}.end")
            self.task_text.config(state=tk.DISABLED)
        else:
            self.selected_index = None
            self.task_text.config(state=tk.NORMAL)
            self.task_text.tag_remove("sel", "1.0", tk.END)
            self.task_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    root.geometry("900x550")
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main() 