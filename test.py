import tkinter as tk
from tkinter import ttk, messagebox, Menu
import json
from datetime import datetime
from tkcalendar import DateEntry

# Create the main window
root = tk.Tk()
root.title("Daily Planner")
root.geometry("500x500")

# Create the notebook to hold the notes
notebook = ttk.Notebook(root)

# Load saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass


# Function to populate the listbox with dates having notes
def populate_date_listbox():
    date_listbox.delete(0, tk.END)  # Clear previous items

    # Collect all dates that have notes
    dates_with_notes = [date for date in notes.keys()]

    # Populate the listbox with these dates
    for date in dates_with_notes:
        date_listbox.insert(tk.END, date)


# Function to add a new note for a specific date
def add_note():
    # Create a new tab for the note
    note_frame = ttk.Frame(notebook)
    notebook.add(note_frame, text="New Note")

    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    date_label = ttk.Label(note_frame, text="Date:")
    date_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

    date_entry = DateEntry(note_frame, date_pattern="yyyy-mm-dd")
    date_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create a function to save the note
    def save_note():
        # Get the title, content, and date of the note
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        date_str = date_entry.get_date().strftime("%Y-%m-%d")

        # Add the note to the notes dictionary under the date key
        notes.setdefault(date_str, []).append({"title": title, "content": content.strip()})

        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

        # Add the note to the notebook
        note_content = tk.Text(notebook, width=40, height=10)
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    # Add a save button to the note frame
    save_button = ttk.Button(note_frame, text="Save", command=save_note)
    save_button.grid(row=3, column=1, padx=10, pady=10)


def get_selected_note_title():
    # Получаем индекс текущей вкладки
    current_tab = notebook.index(notebook.select())

    # Получаем заголовок заметки из текста вкладки
    note_title = notebook.tab(current_tab, "text")

    # Получаем содержимое заметки из соответствующего виджета tk.Text
    note_content_widget = notebook.nametowidget(notebook.select())
    note_content = note_content_widget.get("1.0", tk.END)

    return note_title


def get_selected_note_content():
    # Получаем содержимое заметки из соответствующего виджета tk.Text
    note_content_widget = notebook.nametowidget(notebook.select())
    note_content = note_content_widget.get("1.0", tk.END)

    return note_content


# Получаем дату заметки из словаря notes, используя заголовок заметки
def get_selected_note_data():

    for date, note_list in notes.items():
        for note in note_list:
            if note["title"] == get_selected_note_title():
                note_date = date
                break
    return note_date


def edit_note():
    # Получаем заголовок, содержимое и дату выбранной заметки
    title = get_selected_note_title()
    content = get_selected_note_content()
    date_str = get_selected_note_data()

    # Ищем заметку в словаре notes по заголовку и дате
    for note in notes.get(date_str, []):
        if note["title"] == title:
            # Обновляем заголовок и содержимое заметки
            note["title"] = title
            note["content"] = content.strip()

    # Сохраняем обновленные данные в файл
    with open("notes.json", "w") as f:
        json.dump(notes, f)

    # Переименовываем вкладку в notebook с новым заголовком
    current_tab = notebook.index(notebook.select())
    notebook.tab(current_tab, text=title)


edit_button = ttk.Button(root, text="Сохранить изменения", command=edit_note)
edit_button.pack(padx=10, pady=10)


# Function to load notes for a specific date
def load_notes(date_str):
    global notes  # Add this line to use the global variable
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)

        if date_str in notes:
            for note in notes[date_str]:
                # Add the note to the notebook
                note_content = tk.Text(notebook, width=40, height=10)
                note_content.insert(tk.END, note["content"])
                notebook.add(note_content, text=note["title"])

    except FileNotFoundError:

        # If the file does not exist, do nothing
        pass


# Function to delete a note
def delete_note():
    # Get the current tab index
    current_tab = notebook.index(notebook.select())

    # Get the title of the note to be deleted
    note_title = notebook.tab(current_tab, "text")

    # Show a confirmation dialog
    confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete {note_title}?")

    if confirm:
        # Remove the note from the notebook
        notebook.forget(current_tab)

        # Find and remove the note from the notes dictionary
        keys_to_delete = []
        for date, note_list in notes.items():
            for note in note_list:
                if note["title"] == note_title:
                    note_list.remove(note)
                    if not note_list:
                        keys_to_delete.append(date)

        for date in keys_to_delete:
            del notes[date]
        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)


# Add buttons to the main window
new_button = ttk.Button(root, text="New Note", command=add_note)
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete", command=delete_note)
delete_button.pack(side=tk.LEFT, padx=10, pady=10)
# Create a DateEntry widget for selecting the date
date_label = ttk.Label(root, text="Select Date:")
date_label.pack(padx=10, pady=5)


# Function to load notes for a specific date
def load_notes(date_str):
    global notes
    # Clear current notes by forgetting all tabs
    for tab_id in notebook.tabs():
        notebook.forget(tab_id)

    if date_str in notes:
        for note in notes[date_str]:
            # Add the note to the notebook
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, note["content"])
            notebook.add(note_content, text=note["title"])


# Function to load notes for a specific date
def load_notes_for_date(event=None):
    selected_index = date_listbox.curselection()
    if selected_index:
        date_str = date_listbox.get(selected_index)
        load_notes(date_str)


# создаем меню
menu = Menu(root)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Новая заметка', command=add_note)
new_item.add_separator()
new_item.add_command(label='Сохранить изменения', command=edit_note)
new_item.add_separator()
new_item.add_command(label='Удалить заметку', command=delete_note)

menu.add_cascade(label='Файл', menu=new_item)


root.config(menu=menu)

# Call the load_notes function when the app starts
today_date_str = datetime.today().strftime("%Y-%m-%d")
load_notes(today_date_str)


date_listbox = tk.Listbox(root, width=20, height=10)
date_listbox.pack(padx=10, pady=10)

scrollbar = ttk.Scrollbar(orient="vertical", command=date_listbox.yview)
scrollbar.pack(side='right', fill='y')
date_listbox["yscrollcommand"] = scrollbar.set

populate_date_listbox()  # Populate the listbox with dates
date_listbox.bind("<Double-Button-1>", load_notes_for_date)  # Load notes on double-click


notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
root.mainloop()
