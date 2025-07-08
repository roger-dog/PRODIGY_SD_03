import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap import ttk
import csv
import re  # For email validation

# Initialize Window
root = tk.Tk()
root.title("Contact Management System")
root.geometry("600x400")

# Apply Theme
style = Style("flatly")

# ==== Contact Form ====
frame_form = ttk.LabelFrame(root, text="Add / Edit Contact", padding=10)
frame_form.pack(fill='x', padx=10, pady=10)

ttk.Label(frame_form, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = ttk.Entry(frame_form)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_form, text="Email").grid(row=1, column=0, padx=5, pady=5)
entry_email = ttk.Entry(frame_form)
entry_email.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_form, text="Phone").grid(row=2, column=0, padx=5, pady=5)
entry_phone = ttk.Entry(frame_form)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

# ==== Button Panel ====
frame_buttons = ttk.Frame(root, padding=10)
frame_buttons.pack()

btn_add = ttk.Button(frame_buttons, text="Add Contact")
btn_add.grid(row=0, column=0, padx=5)

btn_edit = ttk.Button(frame_buttons, text="Edit Contact")
btn_edit.grid(row=0, column=1, padx=5)

btn_delete = ttk.Button(frame_buttons, text="Delete Contact")
btn_delete.grid(row=0, column=2, padx=5)

btn_export = ttk.Button(frame_buttons, text="Export to CSV")
btn_export.grid(row=0, column=3, padx=5)

btn_import = ttk.Button(frame_buttons, text="Import from CSV")
btn_import.grid(row=0, column=4, padx=5)

# ==== Contact Display Table ====
frame_table = ttk.LabelFrame(root, text="Saved Contacts", padding=10)
frame_table.pack(fill='both', expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame_table, columns=("Name", "Email", "Phone"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.pack(fill='both', expand=True)

# ==== Helper Functions ====
def clear_form():
    entry_name.delete(0, "end")
    entry_email.delete(0, "end")
    entry_phone.delete(0, "end")

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# ==== Contact Functions ====
def add_contact():
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    for contact in tree.get_children():
        contact_info = tree.item(contact)['values']
        if contact_info[0] == name and contact_info[1] == email and contact_info[2] == phone:
            messagebox.showwarning("Duplicate", "This contact already exists.")
            return

    tree.insert("", "end", values=(name, email, phone))
    clear_form()
    messagebox.showinfo("Success", "Contact added!")

def edit_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a contact to edit.")
        return

    name = entry_name.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    tree.item(selected, values=(name, email, phone))
    clear_form()
    messagebox.showinfo("Success", "Contact updated!")

def delete_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a contact to delete.")
        return

    confirm = messagebox.askyesno("Delete Contact", "Are you sure?")
    if confirm:
        tree.delete(selected)
        clear_form()
        messagebox.showinfo("Deleted", "Contact deleted.")

def export_contacts():
    contacts = tree.get_children()
    if not contacts:
        messagebox.showwarning("No Data", "No contacts to export.")
        return

    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Phone"])
        for contact in contacts:
            writer.writerow(tree.item(contact)['values'])

    messagebox.showinfo("Success", "Contacts exported to contacts.csv")

def import_contacts():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 3:
                    tree.insert("", "end", values=row)
        messagebox.showinfo("Success", "Contacts loaded from contacts.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "contacts.csv file not found.")

# ==== Button Commands ====
btn_add.config(command=add_contact)
btn_edit.config(command=edit_contact)
btn_delete.config(command=delete_contact)
btn_export.config(command=export_contacts)
btn_import.config(command=import_contacts)

# Run the App
root.mainloop()