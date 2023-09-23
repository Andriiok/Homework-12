import pickle
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @staticmethod
    def validate(value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Phone number must contain 10 digits.")

    def __str__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @staticmethod
    def validate(value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                found = True
                break

        if not found:
            raise ValueError(f"Phone number {old_phone} not found in the record")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()
            next_birthday = datetime(today.year, birthday_date.month, birthday_date.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day)
            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 10  # Задайте розмір сторінки

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def paginate(self):
        records = list(self.data.values())
        for i in range(0, len(records), self.page_size):
            yield records[i:i + self.page_size]

    # Збереження адресної книги на диск
    def save_to_disk(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)

    # Завантаження адресної книги з диска
    @classmethod
    def load_from_disk(cls, file_name):
        try:
            with open(file_name, 'rb') as file:
                data = pickle.load(file)
                address_book = cls()
                address_book.data = data
                return address_book
        except FileNotFoundError:
            return cls()

    # Пошук за номером телефону
    def search_by_phone(self, phone):
        found_records = []
        for record in self.data.values():
            for phone_field in record.phones:
                if phone in phone_field.value:
                    found_records.append(record)
                    break
        return found_records


if __name__ == "__main__":
    file_name = 'address_book.pkl'
    book = AddressBook()

    # Завантажити книгу з диска, якщо вона існує
    book = AddressBook.load_from_disk(file_name)

    john_record = Record("John", "1990-05-15")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane", "1985-10-20")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("How can I help you?")

    while True:
        command = input().strip().lower()

        if command == "good bye" or command == "close" or command == "exit":
            # Зберегти книгу на диск перед виходом
            book.save_to_disk(file_name)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Added contact: {name}, {phone}")
        elif command.startswith("change"):
            _, name, phone = command.split()
            try:
                record = book.find(name)
                record.edit_phone(record.phones[0].value, phone)
                print(f"Changed phone for {name} to {phone}")
            except ValueError as e:
                print(e)
        elif command.startswith("phone"):
            _, name = command.split()
            try:
                record = book.find(name)
                print(f"Phone number for {name}: {record.phones[0]}")
            except ValueError as e:
                print(e)
        elif command == "show all":
            if book.data:
                for record in book.data.values():
                    print(record)
            else:
                print("No contacts found")
        elif command == "show birthday":
            for record in book.data.values():
                if record.birthday:
                    days_left = record.days_to_birthday()
                    print(f"{record.name}'s birthday in {days_left} days")
        elif command.startswith("search phone"):
            _, phone_search = command.split()
            results = book.search_by_phone(phone_search)
            if results:
                print
















