import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from datetime import datetime
import uuid

class FireExtinguisherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fire Extinguisher Checker")

        # Title Label with custom text
        self.title_label = tk.Label(root, text="Fire Extinguisher Checker\nbuilt_by_beck", font=("Helvetica", 16, "bold"), fg="blue")
        self.title_label.pack(pady=10)

        self.extinguishers = []
        self.current_file_path = ""
        self.show_serial_number = False  # Flag for toggling Serial Number column

        # Load and Save Buttons
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Progress", command=self.save_progress)
        self.save_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Monthly Reset", command=self.monthly_reset)
        self.reset_button.pack(pady=5)

        # Search bar for filtering
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var, width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_extinguishers)

        # Toggle Serial Number Visibility Button
        self.toggle_serial_button = tk.Button(root, text="Show Serial Number", command=self.toggle_serial_number)
        self.toggle_serial_button.pack(pady=5)

        # Treeview for displaying data in tabular format
        self.tree = ttk.Treeview(root, columns=("Location", "Barcode", "Serial Number", "Status"), show="headings")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Status", text="Status")

        # Scrollbars for Treeview
        self.tree_scroll_y = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree_scroll_x = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_scroll_y.pack(side="right", fill="y")
        self.tree_scroll_x.pack(side="bottom", fill="x")

        # Pass and Fail Buttons
        self.pass_button = tk.Button(root, text="Pass", command=lambda: self.update_status("Pass"))
        self.pass_button.pack(pady=5)

        self.fail_button = tk.Button(root, text="Fail", command=lambda: self.update_status("Fail"))
        self.fail_button.pack(pady=5)

        # Color tags in Treeview
        self.tree.tag_configure('pass', background='lightgreen')
        self.tree.tag_configure('fail', background='lightcoral')
        self.tree.tag_configure('unchecked', background='white')

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("JSON files", "*.json")])
        if filepath.endswith('.xlsx'):
            self.load_from_excel(filepath)
        elif filepath.endswith('.json'):
            self.load_from_json(filepath)
        else:
            messagebox.showerror("Error", "Unsupported file type")

    def load_from_excel(self, filepath):
        data = pd.read_excel(filepath, sheet_name="Sheet1")
        self.extinguishers = data.to_dict(orient="records")
        for extinguisher in self.extinguishers:
            extinguisher["id"] = str(uuid.uuid4())  # Assign a unique ID
        self.display_extinguishers()

    def load_from_json(self, filepath):
        self.current_file_path = filepath
        with open(filepath, 'r') as file:
            self.extinguishers = json.load(file)
            
            # Add a unique ID if not already present (for backward compatibility)
            for extinguisher in self.extinguishers:
                if "id" not in extinguisher:
                    extinguisher["id"] = str(uuid.uuid4())
                
        self.display_extinguishers()

    def display_extinguishers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Update Treeview columns based on Serial Number visibility
        if self.show_serial_number:
            self.tree["displaycolumns"] = ("Location", "Barcode", "Serial Number", "Status")
        else:
            self.tree["displaycolumns"] = ("Location", "Barcode", "Status")

        # Insert each extinguisher into the Treeview
        for extinguisher in self.extinguishers:
            location_desc = extinguisher.get('Location', 'Unknown Location')
            barcode = extinguisher.get('Barcode', 'Unknown Barcode')
            serial_number = extinguisher.get('Serial Number', 'Unknown Serial')
            status = extinguisher.get('Pass Y/N', 'Unchecked')

            # Define tags for coloring
            tags = ('pass' if status == "Pass" else 'fail' if status == "Fail" else 'unchecked',)
            # Insert data with unique ID as the Treeview item's ID
            if self.show_serial_number:
                self.tree.insert("", "end", iid=extinguisher["id"], values=(location_desc, barcode, serial_number, status), tags=tags)
            else:
                self.tree.insert("", "end", iid=extinguisher["id"], values=(location_desc, barcode, status), tags=tags)

    def filter_extinguishers(self, event=None):
        query = self.search_var.get().lower()
        filtered_extinguishers = [
            ext for ext in self.extinguishers
            if query in str(ext.get('Location', '')).lower() or
               query in str(ext.get('Barcode', '')).lower()
        ]
        self.display_filtered_extinguishers(filtered_extinguishers)

    def display_filtered_extinguishers(self, extinguishers):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for extinguisher in extinguishers:
            location_desc = extinguisher.get('Location', 'Unknown Location')
            barcode = extinguisher.get('Barcode', 'Unknown Barcode')
            serial_number = extinguisher.get('Serial Number', 'Unknown Serial')
            status = extinguisher.get('Pass Y/N', 'Unchecked')
            tags = ('pass' if status == "Pass" else 'fail' if status == "Fail" else 'unchecked',)
            if self.show_serial_number:
                self.tree.insert("", "end", iid=extinguisher["id"], values=(location_desc, barcode, serial_number, status), tags=tags)
            else:
                self.tree.insert("", "end", iid=extinguisher["id"], values=(location_desc, barcode, status), tags=tags)

    def toggle_serial_number(self):
        # Toggle the visibility of the Serial Number column
        self.show_serial_number = not self.show_serial_number
        # Update button text based on visibility
        self.toggle_serial_button.config(text="Show Serial Number" if not self.show_serial_number else "Hide Serial Number")
        # Refresh display
        self.display_extinguishers()

    def update_status(self, new_status):
        selected_item = self.tree.selection()
        if selected_item:
            unique_id = selected_item[0]  # Get the unique ID of the selected Treeview item

            # Update the extinguisher status based on the unique ID
            for extinguisher in self.extinguishers:
                if extinguisher.get('id') == unique_id:  # Match by unique ID
                    extinguisher["Pass Y/N"] = new_status
                    break  # Update only the first matching extinguisher

            # Update the specific item in the Treeview directly
            updated_values = list(self.tree.item(unique_id, "values"))
            if self.show_serial_number:
                updated_values[3] = new_status  # Status is at index 3 if Serial Number is shown
            else:
                updated_values[2] = new_status  # Status is at index 2 if Serial Number is hidden

            tag = 'pass' if new_status == "Pass" else 'fail' if new_status == "Fail" else 'unchecked'
            self.tree.item(unique_id, values=updated_values, tags=(tag,))

    def save_progress(self):
        if self.current_file_path:
            backup_filename = f"{os.path.splitext(self.current_file_path)[0]}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = os.path.join("backup", backup_filename)
            os.makedirs("backup", exist_ok=True)
            with open(backup_path, 'w') as backup_file:
                json.dump(self.extinguishers, backup_file)

            with open(self.current_file_path, 'w') as file:
                json.dump(self.extinguishers, file)
            messagebox.showinfo("Saved", "Progress saved with backup!")

    def monthly_reset(self):
        confirm_reset = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the database?")
        if confirm_reset:
            for extinguisher in self.extinguishers:
                extinguisher["Pass Y/N"] = "Unchecked"
            self.display_extinguishers()
            messagebox.showinfo("Reset", "Monthly reset completed. All statuses set to 'Unchecked'.")

# Main loop
root = tk.Tk()
app = FireExtinguisherApp(root)
root.mainloop()
