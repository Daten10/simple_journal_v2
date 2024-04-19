import tkinter as tk
from tkinter import ttk, messagebox, Menu, PhotoImage, Label, StringVar
from tkinter.messagebox import showinfo
import json
from datetime import datetime
from tkcalendar import DateEntry
from plyer import notification


# создаем главное окно
root = tk.Tk()
root.title("Daily Planner")
root.geometry("660x640")
root.resizable(width=False, height=False)

flag = 0

label_style = ttk.Style()
label_style.configure("My.TLabel",          # имя стиля
                    font="helvetica 11",    # шрифт
                    foreground="#004D40",   # цвет текста
                    padding=10,             # отступы
                    background="#B2DFDB")   # фоновый цвет


label_style = ttk.Style()
label_style.configure("Dark.TLabel",          # имя стиля
                    font="helvetica 11",    # шрифт
                    foreground="#c0c5d1",   # цвет текста
                    padding=10,             # отступы
                    background="#3e3f42")   # фоновый цвет


# функция для создания второго окна
def open_new_window():

    newWindow = tk.Tk()

    position = {"padx": 6, "pady": 6, "anchor": "nw"}
    # sets the title of the
    # Toplevel widget
    newWindow.title("Выбор темы")

    # sets the geometry of toplevel
    newWindow.geometry("200x200")

    Default = "White Theme"
    Picture = "Picture Theme"
    Dark = "Dark Theme"

    # по умолчанию будет выбран элемент с value=java
    classic = StringVar(value=Default)

    default_btn = ttk.Radiobutton(newWindow, text=Default, value=Default, variable=classic, command=theme_color_2)
    default_btn.pack(padx=0, pady=0)

    pic_btn = ttk.Radiobutton(newWindow, text=Picture, value=Picture, variable=classic, command=theme_color_1)
    pic_btn.pack(padx=0, pady=0)

    dark_btn = ttk.Radiobutton(newWindow, text=Dark, value=Dark, variable=classic, command=theme_color_2)
    dark_btn.pack(padx=0, pady=0)






# Load saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass


# Функция для обновления Listbox
def update_listbox():
    date_listbox.delete(0, tk.END)  # Очищаем содержимое Listbox
    for note in notes:
        date_listbox.insert(tk.END, note)  # Добавляем каждую заметку в Listbox


# Function to populate the listbox with dates having notes
def populate_date_listbox():
    date_listbox.delete(0, tk.END)  # Clear previous items

    # Collect all dates that have notes
    dates_with_notes = [date for date in notes.keys()]

    # Populate the listbox with these dates
    for date in dates_with_notes:
        date_listbox.insert(tk.END, date)


# функция для закрытия окна
def exit_btn():
    root.destroy()


def open_info():
    showinfo(title="Успех!", message="Изменения сохранены")


# Function to add a new note for a specific date
def add_note():
    global flag
    # Create a new tab for the note
    note_frame = ttk.Frame(notebook)
    notebook.add(note_frame, text="Новая заметка")

    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(note_frame, text="Название:", style='My.TLabel')
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Содержание:",style='My.TLabel')
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    date_label = ttk.Label(note_frame, text="Дата:",style='My.TLabel')
    date_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

    date_entry = DateEntry(note_frame, date_pattern="yyyy-mm-dd")
    date_entry.grid(row=2, column=1, padx=10, pady=10)

    if flag == 1:
        title_label.config(style='Dark.TLabel')
        content_label.config(style='Dark.TLabel')
        date_label.config(style='Dark.TLabel')
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
        update_listbox()

    # Add a save button to the note frame
    save_button = ttk.Button(note_frame, text="Сохранить", command=save_note)
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
    note_date = 0
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
    open_info()


# Function to delete a note
def delete_note():
    # Get the current tab index
    current_tab = notebook.index(notebook.select())

    # Get the title of the note to be deleted
    note_title = notebook.tab(current_tab, "text")

    # Show a confirmation dialog
    confirm = messagebox.askyesno("Удалить заметку", f"Вы уверены что хотите удалить {note_title}?")

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
        update_listbox()


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


# Function to send notification if notes exist for the selected date
def notify_if_notes_exist(date_str):
    if date_str in notes:
        notes_for_date = notes[date_str]
        for note in notes_for_date:
            notification_title = note["title"]  # Заголовок уведомления
            notification_message = note["content"]  # Описание уведомления
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_icon='pics/notifpic.ico',  # Можно указать путь к иконке
                timeout=10  # Время показа уведомления в секундах
            )


def theme_color_1():
    root.image = PhotoImage(file='pics/bg1.png')
    bg_logo = Label(root, image=root.image)
    bg_logo.place(x=0, y=0, relwidth=1, relheight=1)
    bg_logo.lower()
    root.update()
    root.update_idletasks()


def theme_color_2():
    global flag
    flag = 1
    root['background'] = '#222222'
    edit_button.config(style='Dark.TLabel')
    date_label.config(style='Dark.TLabel')

    root.update()
    root.update_idletasks()


# создаем меню
menu = Menu(root)
new_item = Menu(menu, tearoff=0)
exit_item = Menu(menu, tearoff=0)
theme_item = Menu(menu, tearoff=0)
new_item.add_command(label='Новая заметка', command=add_note, font="helvetica 9")
new_item.add_separator()
new_item.add_command(label='Сохранить изменения', command=edit_note, font="helvetica 9")
new_item.add_separator()
new_item.add_command(label='Удалить заметку', command=delete_note, font="helvetica 9")
exit_item.add_command(label='Выход', command=exit_btn, font="helvetica 9")

theme_item.add_command(label='Темы', command=open_new_window, font="helvetica 9")

menu.add_cascade(label='Файл', menu=new_item, font="helvetica 9")
menu.add_cascade(label='Темы', menu=theme_item, font="helvetica 9")
menu.add_cascade(label='Выход', menu=exit_item, font="helvetica 9")

root.config(menu=menu)

# Create the notebook to hold the notes
notebook = ttk.Notebook(root)

edit_button = ttk.Button(root, text="Сохранить изменения", command=edit_note, style='My.TLabel')
edit_button.pack(side='bottom', padx=10, pady=10)


# Call the load_notes function when the app starts
today_date_str = datetime.today().strftime("%Y-%m-%d")
load_notes(today_date_str)

selected_date = datetime.today().strftime("%Y-%m-%d")
notify_if_notes_exist(selected_date)  # Проверяем и отправляем уведомление

date_label = ttk.Label(root, text="Список заметок:", style='My.TLabel', font='helvetica 11')
date_label.pack(padx=1, pady=1, anchor='ne')

date_listbox = tk.Listbox(root, width=20, height=45)
date_listbox.pack(padx=10, pady=30, side='right')

populate_date_listbox()  # Populate the listbox with dates
date_listbox.bind("<Double-Button-1>", load_notes_for_date)  # Load notes on double-click

notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
