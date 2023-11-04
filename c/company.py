from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('company.db')
cursor = connection.cursor()

# Создаем таблицу Company
cursor.execute('''
CREATE TABLE IF NOT EXISTS Company (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
phone TEXT NOT NULL,
email TEXT NOT NULL,
salary REAL
)
''')
# Функция для добавления сотрудника
def insert_varible_into_table(id, name, phone, email, salary):
    try:
        sqlite_connection = sqlite3.connect('company.db')
        cursor = sqlite_connection.cursor()
        
        sqlite_insert_with_param = """INSERT INTO company
                              (id, name, phone, email, salary)
                              VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (id, name, phone, email, salary)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
       
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
           # print("Соединение с SQLite закрыто")

# Добавляем нового пользователя
insert_varible_into_table(1, 'Ivanov', '+79084406442', 'cd@infosco.com', 10000)
insert_varible_into_table(2, 'Petrov', '+79046296556', 'info@infosco.com', 20000)
insert_varible_into_table(3, 'Sidorov', '+79025564112', 'mama@infosco.com', 25000)
insert_varible_into_table(4, 'Chirkov', '+79026522145', 'vova@infosco.com', 15000)


# отображаем в TREEVIEW
root = Tk()
root.title("Traktorister.project")
root.geometry("350x350") 
 
# определяем данные для отображения
label = ttk.Label()
label.pack(anchor=N, fill=X)

# определяем столбцы
columns = ("id", "name", "phone", "email", "salary")
tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(expand=1, fill=BOTH)
 
# определяем заголовки
tree.heading("id", text="ID", anchor=W)
tree.heading("name", text="Имя", anchor=W)
tree.heading("phone", text="Телефoн", anchor=W)
tree.heading("email", text="Email", anchor=W)
tree.heading("salary", text="Зарплата", anchor=W)
 
tree.column("#1", stretch=NO, width=20)
tree.column("#2", stretch=NO, width=80)
tree.column("#3", stretch=NO, width=80)
tree.column("#4", stretch=NO, width=70)
tree.column("#5", stretch=NO, width=50)
 
# добавляем данные для отображения
cursor.execute('SELECT * FROM company')
people = cursor.fetchall()

for person in people:
    tree.insert("", END, values=person)
 
# определяем выделенную строку
def item_selected(event):
    selected_people = ""
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        person = item["values"]
        selected_people = f"{selected_people}{person}\n"
    label["text"]=selected_people
 
tree.bind("<<TreeviewSelect>>", item_selected)
 
root.mainloop()

# удаление записи с заданным id
def delete_record():
    try:
        sqlite_connection = sqlite3.connect('company.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = """DELETE from company where id = 2"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

delete_record()

# обновление записи с заданным id
import sqlite3

def update_sqlite_table():
    try:
        sqlite_connection = sqlite3.connect('company.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """Update company set salary = 50000 where id = 4"""
        cursor.execute(sql_update_query)
        sqlite_connection.commit()
        print("Запись успешно обновлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

update_sqlite_table()


# Выбираем всех пользователей
cursor.execute('SELECT * FROM company')
users = cursor.fetchall()

# Выводим итоговую БД в консоль
for user in users:
  print(user)
  
# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()