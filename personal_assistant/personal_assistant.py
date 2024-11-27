import json
import csv
import os
from datetime import datetime


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.note_id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(data['id'], data['title'], data['content'], data['timestamp'])


class Task:
    def __init__(self, task_id, title, description, done, priority, due_date):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

    @staticmethod
    def from_dict(data):
        return Task(data['id'], data['title'], data['description'], data['done'], data['priority'], data['due_date'])


class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.contact_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['id'], data['name'], data['phone'], data['email'])


class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.record_id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.record_id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

    @staticmethod
    def from_dict(data):
        return FinanceRecord(data['id'], data['amount'], data['category'], data['date'], data['description'])


def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_from_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def import_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            notes_menu()
        elif choice == '2':
            tasks_menu()
        elif choice == '3':
            contacts_menu()
        elif choice == '4':
            finance_menu()
        elif choice == '5':
            calculator_menu()
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def notes_menu():
    notes = load_from_json('notes.json')
    notes = [Note.from_dict(note) for note in notes]

    while True:
        print("Управление заметками:")
        print("1. Добавить новую заметку")
        print("2. Просмотреть заметки")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Экспорт заметок в CSV")
        print("6. Импорт заметок из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            note_id = len(notes) + 1
            note = Note(note_id, title, content, timestamp)
            notes.append(note)
            save_to_json([note.to_dict() for note in notes], 'notes.json')
            print("Заметка успешно добавлена!")
        elif choice == '2':
            for note in notes:
                print(f"ID: {note.note_id}, Заголовок: {note.title}, Время: {note.timestamp}")
        elif choice == '3':
            note_id = int(input("Введите ID заметки для редактирования: "))
            for note in notes:
                if note.note_id == note_id:
                    note.title = input("Введите новый заголовок: ")
                    note.content = input("Введите новое содержимое: ")
                    note.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    save_to_json([note.to_dict() for note in notes], 'notes.json')
                    print("Заметка успешно отредактирована!")
                    break
            else:
                print("Заметка не найдена.")
        elif choice == '4':
            note_id = int(input("Введите ID заметки для удаления: "))
            notes = [note for note in notes if note.note_id != note_id]
            save_to_json([note.to_dict() for note in notes], 'notes.json')
            print("Заметка успешно удалена!")
        elif choice == '5':
            export_to_csv([note.to_dict() for note in notes], 'notes_export.csv')
            print("Заметки успешно экспортированы в CSV!")
        elif choice == '6':
            imported_notes = import_from_csv('notes_import.csv')
            notes.extend([Note.from_dict(note) for note in imported_notes])
            save_to_json([note.to_dict() for note in notes], 'notes.json')
            print("Заметки успешно импортированы из CSV!")
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def tasks_menu():
    tasks = load_from_json('tasks.json')
    tasks = [Task.from_dict(task) for task in tasks]

    while True:
        print("Управление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
            due_date = input("Введите срок выполнения (в формате ДД-ММ-ГГГГ): ")
            task_id = len(tasks) + 1
            task = Task(task_id, title, description, False, priority, due_date)
            tasks.append(task)
            save_to_json([task.to_dict() for task in tasks], 'tasks.json')
            print("Задача успешно добавлена!")
        elif choice == '2':
            for task in tasks:
                print(
                    f"ID: {task.task_id}, Заголовок: {task.title}, Статус: {'Выполнена' if task.done else 'Не выполнена'}, Приоритет: {task.priority}, Срок: {task.due_date}")
        elif choice == '3':
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            for task in tasks:
                if task.task_id == task_id:
                    task.done = True
                    save_to_json([task.to_dict() for task in tasks], 'tasks.json')
                    print("Задача отмечена как выполненная!")
                    break
            else:
                print("Задача не найдена.")
        elif choice == '4':
            task_id = int(input("Введите ID задачи для редактирования: "))
            for task in tasks:
                if task.task_id == task_id:
                    task.title = input("Введите новое название задачи: ")
                    task.description = input("Введите новое описание задачи: ")
                    task.priority = input("Выберите новый приоритет (Высокий/Средний/Низкий): ")
                    task.due_date = input("Введите новый срок выполнения (в формате ДД-ММ-ГГГГ): ")
                    save_to_json([task.to_dict() for task in tasks], 'tasks.json')
                    print("Задача успешно отредактирована!")
                    break
            else:
                print("Задача не найдена.")
        elif choice == '5':
            task_id = int(input("Введите ID задачи для удаления: "))
            tasks = [task for task in tasks if task.task_id != task_id]
            save_to_json([task.to_dict() for task in tasks], 'tasks.json')
            print("Задача успешно удалена!")
        elif choice == '6':
            export_to_csv([task.to_dict() for task in tasks], 'tasks_export.csv')
            print("Задачи успешно экспортированы в CSV!")
        elif choice == '7':
            imported_tasks = import_from_csv('tasks_import.csv')
            tasks.extend([Task.from_dict(task) for task in imported_tasks])
            save_to_json([task.to_dict() for task in tasks], 'tasks.json')
            print("Задачи успешно импортированы из CSV!")
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def contacts_menu():
    contacts = load_from_json('contacts.json')
    contacts = [Contact.from_dict(contact) for contact in contacts]

    while True:
        print("Управление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Экспорт контактов в CSV")
        print("6. Импорт контактов из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона: ")
            email = input("Введите адрес электронной почты: ")
            contact_id = len(contacts) + 1
            contact = Contact(contact_id, name, phone, email)
            contacts.append(contact)
            save_to_json([contact.to_dict() for contact in contacts], 'contacts.json')
            print("Контакт успешно добавлен!")
        elif choice == '2':
            query = input("Введите имя или номер телефона для поиска: ")
            found_contacts = [contact for contact in contacts if query in contact.name or query in contact.phone]
            for contact in found_contacts:
                print(
                    f"ID: {contact.contact_id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")
        elif choice == '3':
            contact_id = int(input("Введите ID контакта для редактирования: "))
            for contact in contacts:
                if contact.contact_id == contact_id:
                    contact.name = input("Введите новое имя: ")
                    contact.phone = input("Введите новый номер телефона: ")
                    contact.email = input("Введите новый адрес электронной почты: ")
                    save_to_json([contact.to_dict() for contact in contacts], 'contacts.json')
                    print("Контакт успешно отредактирован!")
                    break
            else:
                print("Контакт не найден.")
        elif choice == '4':
            contact_id = int(input("Введите ID контакта для удаления: "))
            contacts = [contact for contact in contacts if contact.contact_id != contact_id]
            save_to_json([contact.to_dict() for contact in contacts], 'contacts.json')
            print("Контакт успешно удален!")
        elif choice == '5':
            export_to_csv([contact.to_dict() for contact in contacts], 'contacts_export.csv')
            print("Контакты успешно экспортированы в CSV!")
        elif choice == '6':
            imported_contacts = import_from_csv('contacts_import.csv')
            contacts.extend([Contact.from_dict(contact) for contact in imported_contacts])
            save_to_json([contact.to_dict() for contact in contacts], 'contacts.json')
            print("Контакты успешно импортированы из CSV!")
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def finance_menu():
    finance_records = load_from_json('finance.json')
    finance_records = [FinanceRecord.from_dict(record) for record in finance_records]

    while True:
        print("Управление финансовыми записями:")
        print("1. Добавить новую запись")
        print("2. Просмотреть все записи")
        print("3. Генерация отчёта")
        print("4. Удалить запись")
        print("5. Экспорт финансовых записей в CSV")
        print("6. Импорт финансовых записей из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            amount = float(
                input("Введите сумму операции (положительное число для доходов, отрицательное для расходов): "))
            category = input("Введите категорию операции: ")
            date = input("Введите дату операции (в формате ДД-ММ-ГГГГ): ")
            description = input("Введите описание операции: ")
            record_id = len(finance_records) + 1
            record = FinanceRecord(record_id, amount, category, date, description)
            finance_records.append(record)
            save_to_json([record.to_dict() for record in finance_records], 'finance.json')
            print("Финансовая запись успешно добавлена!")
        elif choice == '2':
            for record in finance_records:
                print(
                    f"ID: {record.record_id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")
        elif choice == '3':
            start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
            end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
            filtered_records = [record for record in finance_records if start_date <= record.date <= end_date]
            total_income = sum(record.amount for record in filtered_records if record.amount > 0)
            total_expenses = sum(record.amount for record in filtered_records if record.amount < 0)
            balance = total_income + total_expenses
            print(f"Финансовый отчёт за период с {start_date} по {end_date}:")
            print(f"- Общий доход: {total_income} руб.")
            print(f"- Общие расходы: {total_expenses} руб.")
            print(f"- Баланс: {balance} руб.")
            report_filename = f"report_{start_date}_{end_date}.csv"
            export_to_csv([record.to_dict() for record in filtered_records], report_filename)
            print(f"Подробная информация сохранена в файле {report_filename}")
        elif choice == '4':
            record_id = int(input("Введите ID записи для удаления: "))
            finance_records = [record for record in finance_records if record.record_id != record_id]
            save_to_json([record.to_dict() for record in finance_records], 'finance.json')
            print("Финансовая запись успешно удалена!")
        elif choice == '5':
            export_to_csv([record.to_dict() for record in finance_records], 'finance_export.csv')
            print("Финансовые записи успешно экспортированы в CSV!")
        elif choice == '6':
            imported_records = import_from_csv('finance_import.csv')
            finance_records.extend([FinanceRecord.from_dict(record) for record in imported_records])
            save_to_json([record.to_dict() for record in finance_records], 'finance.json')
            print("Финансовые записи успешно импортированы из CSV!")
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def calculator_menu():
    while True:
        print("Калькулятор:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Назад")
        choice = input("Выберите действие: ")

        if choice == '5':
            break

        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))

            if choice == '1':
                result = num1 + num2
                print(f"Результат: {result}")
            elif choice == '2':
                result = num1 - num2
                print(f"Результат: {result}")
            elif choice == '3':
                result = num1 * num2
                print(f"Результат: {result}")
            elif choice == '4':
                if num2 == 0:
                    print("Ошибка: деление на ноль.")
                else:
                    result = num1 / num2
                    print(f"Результат: {result}")
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Ошибка: введите корректные числа.")


if __name__ == "__main__":
    main_menu()
