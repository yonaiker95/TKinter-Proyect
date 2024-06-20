import tkinter as tk
from tkinter import messagebox
import sqlite3

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD App with SQLite")
        
        self.create_widgets()
        self.create_db()
    
    def create_widgets(self):
        # Labels and Entries
        self.id_label = tk.Label(self.root, text="ID")
        self.id_label.grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.name_label = tk.Label(self.root, text="Name")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.age_label = tk.Label(self.root, text="Age")
        self.age_label.grid(row=2, column=0, padx=10, pady=10)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        self.create_button = tk.Button(self.root, text="Create", command=self.create_record)
        self.create_button.grid(row=3, column=0, pady=10)
        
        self.read_button = tk.Button(self.root, text="Read", command=self.read_records)
        self.read_button.grid(row=3, column=1, pady=10)
        
        self.update_button = tk.Button(self.root, text="Update", command=self.update_record)
        self.update_button.grid(row=4, column=0, pady=10)
        
        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_record)
        self.delete_button.grid(row=4, column=1, pady=10)
        
        self.records_text = tk.Text(self.root, height=10, width=50)
        self.records_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    
    def create_db(self):
        self.conn = sqlite3.connect('crud_app.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL)''')
        self.conn.commit()
    
    def create_record(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        if name and age:
            self.cursor.execute("INSERT INTO records (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
            messagebox.showinfo("Success", "Record created successfully")
            self.clear_entries()
            self.read_records()
        else:
            messagebox.showwarning("Input Error", "Please enter both name and age.")
    
    def read_records(self):
        self.cursor.execute("SELECT * FROM records")
        records = self.cursor.fetchall()
        self.records_text.delete(1.0, tk.END)
        for record in records:
            self.records_text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}\n")
    
    def update_record(self):
        record_id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        if record_id and name and age:
            self.cursor.execute("UPDATE records SET name = ?, age = ? WHERE id = ?", (name, age, record_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Record updated successfully")
            self.clear_entries()
            self.read_records()
        else:
            messagebox.showwarning("Input Error", "Please enter ID, name, and age.")
    
    def delete_record(self):
        record_id = self.id_entry.get()
        if record_id:
            self.cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully")
            self.clear_entries()
            self.read_records()
        else:
            messagebox.showwarning("Input Error", "Please enter the ID.")
    
    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
