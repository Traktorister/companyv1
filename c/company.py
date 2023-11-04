import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Соединение с базой данных
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Создание таблицы сотрудников
cursor.execute('''CREATE TABLE IF NOT EXISTS company
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 phone TEXT,
                 email TEXT,
                 salary REAL)''')

# Функция для добавления сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if name and phone and email and salary:
        cursor.execute('''INSERT INTO company (name, phone, email, salary)
                        VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        conn.commit()
        messagebox.showinfo('Success', 'Сотрудник добавлен успешно.')
        clear_entries()
        load_employees()
    else:
        messagebox.showerror('Error', 'Пожалуйста, заполните все поля.')

# Функция для изменения сотрудникаf
def update_employee():
    selected_item = treeview.selection()
    if selected_item:
        employee_id = treeview.item(selected_item)['values'][0]
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()

        if name and phone and email and salary:
            cursor.execute('''UPDATE company SET name=?, phone=?, email=?, salary=?
                            WHERE id=?''', (name, phone, email, salary, employee_id))
            cursor.commit()
            messagebox.showinfo('Success', 'Сотрудник обновлен успешно.')
            clear_entries()
            load_employees()
        else:
            messagebox.showerror('Error', 'Пожалуйста, заполните все поля.')
    else:
        messagebox.showerror('Error', 'Пожалуйста, выберите сотрудника для изменения.')

# Функция для удаления сотрудника
def delete_employee():
    selected_item = treeview.selection()
    if selected_item:
        result = messagebox.askyesno('Confirmation', 'Вы уверены, что хотите удалить выбранного сотрудника?')
        if result:
            employee_id = treeview.item(selected_item)['values'][0]
            cursor.execute('DELETE FROM company WHERE id=?', (employee_id,))
            cursor.commit()
            messagebox.showinfo('Success', 'Сотрудник удален успешно.')
            clear_entries()
            load_employees()
    else:
        messagebox.showerror('Error', 'Пожалуйста, выберите сотрудника для удаления.')

# Функция для поиска сотрудника
def search_employee():
    keyword = search_entry.get()
    if keyword:
        cursor.execute("SELECT * FROM company WHERE name LIKE ?", ('%' + keyword + '%',))
        rows = cursor.fetchall()
        if rows:
            clear_treeview()
            for row in rows:
                treeview.insert('', 'end', values=row)
        else:
            messagebox.showinfo('No Results', 'Сотрудники с таким именем не найдены.')
    else:
        messagebox.showerror('Error', 'Пожалуйста, введите ключевое слово для поиска.')

# Функция для очистки полей
def clear_entries():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    salary_entry.delete(0, 'end')

# Функция для загрузки сотрудников в Treeview
    cursor.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM employees')
    for row in cursor:
        treeview.insert('', 'end', values=row)

# Функция для очистки Treeview
def clear_treeview():
    records = treeview.get_children()
    for record in records:
        treeview.delete(record)

# Создание графического интерфейса
root = tk.Tk()
root.title('Список сотрудников компании')

conn.commit()
conn.close()
