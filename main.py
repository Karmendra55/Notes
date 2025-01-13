import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style

# For main software
root = tk.Tk()
root.title("Personal Notes")
root.geometry("600x600")  # Adjusted size for better layout
style = Style(theme='darkly')  # Use 'darkly' theme for dark background

# Configure tab font to be Bold
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"), foreground="white", background="#444444")

# Configure background and text color for all widgets
style.configure("TFrame", background="#17161b")  # Dark background for frames
style.configure("TLabel", foreground="white", background="#17161b")  # White text for labels
style.configure("TEntry", foreground="white", background="#444444", fieldbackground="#444444")  # White text for entry and dark background
style.configure("TButton", foreground="white", background="#444444", borderwidth=1, focusthickness=3)  # White text for buttons and dark background

# Notebook to hold notes
notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Load Saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

# Function for new notes
def add_notes():
    note_frame = ttk.Frame(notebook, padding=15)
    notebook.add(note_frame, text="New Note")
    
    title_label = ttk.Label(note_frame, text="Title:", font=("Helvetica", 12, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky='W')
    
    title_entry = ttk.Entry(note_frame, width=40, font=("Helvetica", 12))
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    
    content_label = ttk.Label(note_frame, text="Content:", font=("Helvetica", 12, "bold"))
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    
    content_entry = tk.Text(note_frame, width=40, height=10, font=("Helvetica", 12), fg="white", bg="#444444")
    content_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Function to save
    def save_note():
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        
        # Add to dictionary
        notes[title] = content.strip()
        
        # Save the dictionary
        with open("notes.json", "w") as f:
            json.dump(notes, f)
            
        # Add notes to notebook
        note_content = tk.Text(notebook, width=40, height=10, font=("Helvetica", 12), fg="white", bg="#444444")
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)
        
    # Add save button
    save_button = ttk.Button(note_frame, text="Save", command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)

# Function to load notes
def load_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
                
        for title, content in notes.items():
            # Add notes
            note_content = tk.Text(notebook, width=40, height=10, font=("Helvetica", 12), fg="white", bg="#444444")
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)
                
    except FileNotFoundError:
        pass

# Calling the load notes function
load_notes()

# For deleting the notes
def delete_note():
    current_tab = notebook.index(notebook.select())
    
    note_title = notebook.tab(current_tab, "text")
    
    # Show confirmation
    confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete this note: {note_title}?")
    
    if confirm:
        notebook.forget(current_tab)
        notes.pop(note_title)
        with open("notes.json", "w") as f:
            json.dump(notes, f)

# Adding buttons with better style
button_style = "info.TButton"
new_button = ttk.Button(root, text="New Note", command=add_notes, style=button_style)
new_button.pack(side=tk.LEFT, padx=20, pady=10)

delete_button = ttk.Button(root, text="Delete", command=delete_note, style="danger.TButton")
delete_button.pack(side=tk.LEFT, padx=20, pady=10)

# Add padding to the root window for better UI
root.config(padx=20, pady=20, bg="#17161b")

root.mainloop()
