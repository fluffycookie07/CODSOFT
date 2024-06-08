import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Task:
    def __init__(self, title, description, completed=False):
        self.title = title
        self.description = description
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.title}: {self.description} [{status}]"

class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, index, title, description):
        if 0 <= index < len(self.tasks):
            self.tasks[index].title = title
            self.tasks[index].description = description
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
                self.tasks = [Task(**task) for task in tasks]
        except FileNotFoundError:
            pass

class ToDoApp:
    def __init__(self, root):
        self.todo_list = ToDoList()
        self.root = root
        self.root.title("To-Do List Application")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.listbox = tk.Listbox(self.frame, width=50, height=10)
        self.listbox.pack(side=tk.LEFT, padx=10)
        
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.load_tasks_to_listbox()
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.update_button = tk.Button(self.button_frame, text="Update Task", command=self.update_task)
        self.update_button.grid(row=0, column=1, padx=5)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)
        
        self.complete_button = tk.Button(self.button_frame, text="Mark Completed", command=self.mark_task_completed)
        self.complete_button.grid(row=0, column=3, padx=5)

    def load_tasks_to_listbox(self):
        self.listbox.delete(0, tk.END) 
        for i, task in enumerate(self.todo_list.tasks):
            self.listbox.insert(tk.END, f"{i}. {task}")

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        description = simpledialog.askstring("Add Task", "Enter task description:")
        if title and description:
            self.todo_list.add_task(title, description)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Input Error", "Title and description cannot be empty!")

    def update_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0] 
            title = simpledialog.askstring("Update Task", "Enter new task title:", initialvalue=self.todo_list.tasks[index].title)
            description = simpledialog.askstring("Update Task", "Enter new task description:", initialvalue=self.todo_list.tasks[index].description)
            if title and description:
                self.todo_list.update_task(index, title, description)
                self.load_tasks_to_listbox()
            else:
                messagebox.showwarning("Input Error", "Title and description cannot be empty!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to update.")

    def delete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0] 
            self.todo_list.delete_task(index)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_task_completed(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0] 
            self.todo_list.mark_task_completed(index)
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
