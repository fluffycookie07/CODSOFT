import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

class Contact:
    def __init__(self, name, phone_number, email, address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name}: {self.phone_number}"

class ContactBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.init_ui()

    def init_ui(self):
        self.add_button = ttk.Button(self, text="Add Contact", command=self.add_contact)
        self.view_button = ttk.Button(self, text="View Contacts", command=self.view_contacts)
        self.search_button = ttk.Button(self, text="Search Contact", command=self.search_contact)
        self.update_button = ttk.Button(self, text="Update Contact", command=self.update_contact)
        self.delete_button = ttk.Button(self, text="Delete Contact", command=self.delete_contact)

        self.contact_list = tk.Listbox(self, height=10)
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.contact_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contact_list.yview)

        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.view_button.grid(row=0, column=1, padx=10, pady=10)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
        self.update_button.grid(row=0, column=3, padx=10, pady=10)
        self.delete_button.grid(row=0, column=4, padx=10, pady=10)

        self.contact_list.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.scrollbar.grid(row=1, column=5, padx=10, pady=10, sticky="ns")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.contacts = []

    def add_contact(self):
        dialog = ContactDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            contact = dialog.result
            self.contacts.append(contact)
            self.update_contact_list()

    def view_contacts(self):
        self.update_contact_list()

    def search_contact(self):
        search_term = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if search_term:
            self.contact_list.delete(0, tk.END)
            for contact in self.contacts:
                if search_term.lower() in contact.name.lower() or search_term in contact.phone_number:
                    self.contact_list.insert(tk.END, str(contact))

    def update_contact(self):
        selected_index = self.contact_list.curselection()
        if selected_index:
            index = selected_index[0]
            contact = self.contacts[index]
            dialog = ContactDialog(self, contact)
            self.wait_window(dialog)
            if dialog.result:
                self.contacts[index] = dialog.result
                self.update_contact_list()
        else:
            messagebox.showwarning("Warning", "No contact selected.")

    def delete_contact(self):
        selected_index = self.contact_list.curselection()
        if selected_index:
            index = selected_index[0]
            del self.contacts[index]
            self.update_contact_list()
        else:
            messagebox.showwarning("Warning", "No contact selected.")

    def update_contact_list(self):
        self.contact_list.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_list.insert(tk.END, str(contact))

class ContactDialog(tk.Toplevel):
    def __init__(self, parent, contact=None):
        super().__init__(parent)
        self.result = None
        self.contact = contact
        self.init_ui()

    def init_ui(self):
        self.title("Add Contact" if not self.contact else "Update Contact")

        self.name_label = ttk.Label(self, text="Name:")
        self.name_entry = ttk.Entry(self)
        self.phone_label = ttk.Label(self, text="Phone Number:")
        self.phone_entry = ttk.Entry(self)
        self.email_label = ttk.Label(self, text="Email:")
        self.email_entry = ttk.Entry(self)
        self.address_label = ttk.Label(self, text="Address:")
        self.address_entry = ttk.Entry(self)

        if self.contact:
            self.name_entry.insert(0, self.contact.name)
            self.phone_entry.insert(0, self.contact.phone_number)
            self.email_entry.insert(0, self.contact.email)
            self.address_entry.insert(0, self.contact.address)

        self.ok_button = ttk.Button(self, text="OK", command=self.on_ok)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.on_cancel)

        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.phone_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.email_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.ok_button.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.cancel_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def on_ok(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone_number:
            self.result = Contact(name, phone_number, email, address)
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Name and Phone Number are required.")

    def on_cancel(self):
        self.destroy()

if __name__ == "__main__":
    app = ContactBook()
    app.mainloop()
