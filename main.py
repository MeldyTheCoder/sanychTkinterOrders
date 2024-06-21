import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import mysql.connector


def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="repair_requests"
    )

    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS requests (id INT NOT NULL AUTO_INCREMENT, equipment_type VARCHAR(255), serial_number VARCHAR(255), problem_description TEXT, priority VARCHAR(255), status VARCHAR(255), PRIMARY KEY (id))',
        ()
    )
    print('connectedf')
    connection.commit()
    return connection


def register_request():
    def save_request():
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requests (equipment_type, serial_number, problem_description, priority, status) VALUES (%s, %s, %s, %s, %s)",
                           (type_entry.get(), serial_entry.get(), description_entry.get(), priority_entry.get(), 'New'))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заявка успешно зарегистрирована")
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка", f"Ошибка: {err}")
        finally:
            register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Регистрация заявки")
    register_window.geometry("500x400")
    register_window.configure(bg='#f0f0f0')

    ttk.Label(register_window, text="Тип оборудования").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(register_window, text="Серийный номер").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(register_window, text="Описание проблемы").grid(row=2, column=0, padx=10, pady=10)
    ttk.Label(register_window, text="Приоритет").grid(row=3, column=0, padx=10, pady=10)

    type_entry = ttk.Entry(register_window)
    serial_entry = ttk.Entry(register_window)
    description_entry = ttk.Entry(register_window)
    priority_entry = ttk.Entry(register_window)

    type_entry.grid(row=0, column=1, padx=10, pady=10)
    serial_entry.grid(row=1, column=1, padx=10, pady=10)
    description_entry.grid(row=2, column=1, padx=10, pady=10)
    priority_entry.grid(row=3, column=1, padx=10, pady=10)

    save_button = ttk.Button(register_window, text="Сохранить", command=save_request)
    save_button.grid(row=4, column=1, pady=20)


def process_request():
    def update_request():
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE requests SET status=%s WHERE id=%s", (status_entry.get(), id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заявка успешно обновлена")
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка", f"Ошибка: {err}")
        finally:
            process_window.destroy()

    process_window = tk.Toplevel(root)
    process_window.title("Обработка заявки")
    process_window.geometry("400x300")
    process_window.configure(bg='#f0f0f0')

    ttk.Label(process_window, text="ID заявки").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(process_window, text="Статус").grid(row=1, column=0, padx=10, pady=10)

    id_entry = ttk.Entry(process_window)
    status_entry = ttk.Entry(process_window)

    id_entry.grid(row=0, column=1, padx=10, pady=10)
    status_entry.grid(row=1, column=1, padx=10, pady=10)

    update_button = ttk.Button(process_window, text="Обновить", command=update_request)
    update_button.grid(row=2, column=1, pady=20)


def generate_report():
    report_window = tk.Toplevel(root)
    report_window.title("Отчет о выполненных заявках")
    report_window.geometry("800x600")
    report_window.configure(bg='#f0f0f0')

    tree = ttk.Treeview(report_window, columns=("ID", "Тип оборудования", "Серийный номер", "Описание", "Приоритет", "Статус", "Создано", "Обновлено"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Тип оборудования", text="Тип оборудования")
    tree.heading("Серийный номер", text="Серийный номер")
    tree.heading("Описание", text="Описание")
    tree.heading("Приоритет", text="Приоритет")
    tree.heading("Статус", text="Статус")
    tree.heading("Создано", text="Создано")
    tree.heading("Обновлено", text="Обновлено")
    tree.pack(fill="both", expand=True)

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests WHERE status='Completed'")
        requests = cursor.fetchall()
        for request in requests:
            tree.insert('', 'end', values=request)
        conn.close()
    except mysql.connector.Error as err:
        report_text = scrolledtext.ScrolledText(report_window, width=110, height=30)
        report_text.insert(tk.END, f"Ошибка при получении данных из базы данных: {err}")
        report_text.pack(fill="both", expand=True)


root = tk.Tk()
root.title("Учет заявок на ремонт")
root.geometry("600x400")
root.configure(bg='#e0e0e0')

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10, width=20)
style.configure('TLabel', font=('Helvetica', 14), background='#e0e0e0')
style.configure('TEntry', font=('Helvetica', 12), background='#f0f0f0')

register_button = ttk.Button(root, text="Зарегистрировать заявку", command=register_request)
process_button = ttk.Button(root, text="Обработать заявку", command=process_request)
report_button = ttk.Button(root, text="Создать отчет", command=generate_report)

register_button.pack(pady=20)
process_button.pack(pady=20)
report_button.pack(pady=20)

root.mainloop()