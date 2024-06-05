import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Task:
    def __init__(self, title, description=''):
        self.title = title
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "Complete" if self.completed else "Incomplete"
        return f"{self.title} - {self.description} [{status}]"

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def update_task(self, index, title=None, description=None):
        if 0 <= index < len(self.tasks):
            if title:
                self.tasks[index].title = title
            if description:
                self.tasks[index].description = description

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def view_tasks(self):
        return [str(task) for task in self.tasks]

    def save_to_file(self, filename='data.json'):
        with open(filename, 'w') as file:
            tasks_data = [{'title': task.title, 'description': task.description, 'completed': task.completed} for task in self.tasks]
            json.dump(tasks_data, file)

    def load_from_file(self, filename='data.json'):
        try:
            with open(filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(data['title'], data['description']) for data in tasks_data]
                for i, task in enumerate(self.tasks):
                    if tasks_data[i]['completed']:
                        task.mark_complete()
        except FileNotFoundError:
            self.tasks = []

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.todo_list = ToDoList()
        self.todo_list.load_from_file()

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.task_listbox.pack(pady=10)

        self.load_tasks()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Complete", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(pady=5)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task_str in self.todo_list.view_tasks():
            self.task_listbox.insert(tk.END, task_str)

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        description = simpledialog.askstring("Add Task", "Enter task description:")
        if title:
            task = Task(title, description)
            self.todo_list.add_task(task)
            self.load_tasks()

    def update_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            current_task = self.todo_list.tasks[index]
            title = simpledialog.askstring("Update Task", "Enter new task title:", initialvalue=current_task.title)
            description = simpledialog.askstring("Update Task", "Enter new task description:", initialvalue=current_task.description)
            self.todo_list.update_task(index, title, description)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Update Task", "Please select a task to update.")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo_list.delete_task(index)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo_list.mark_task_complete(index)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Complete Task", "Please select a task to mark as complete.")

    def save_tasks(self):
        self.todo_list.save_to_file()
        messagebox.showinfo("Save Tasks", "Tasks saved successfully.")

    def load_tasks(self):
        self.todo_list.load_from_file()
        self.task_listbox.delete(0, tk.END)
        for task_str in self.todo_list.view_tasks():
            self.task_listbox.insert(tk.END, task_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
