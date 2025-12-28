from abc import ABC, abstractmethod
from datetime import datetime

class ItemNotAvailableError(Exception): # pozycja jest już wypożyczona
    pass
class UserLimitExceededError(Exception): # użytkownik przekroczył limit wypożyczeń
    pass
class InvalidItemError(Exception): # pozycja nie istnieje w systemie
    pass
class InvalidUserError(Exception): # użytkownik nie jest zarejestrowany
    pass

class LibraryItem(ABC):
    def __init__(self, title, author, year, item_id):
        self._title = title
        self._author = author
        self._year = year
        self._item_id = item_id
        self._is_available = True

    @property
    def title(self):
        return self._title

    @abstractmethod
    def get_rental_period(self):
        pass

    @property
    def author(self):
        return self._author
    
    @property
    def year(self):
        return self._year

    @property
    def item_id(self):
        return self._item_id
    
    @property
    def is_available(self):
        return self._is_available

    @abstractmethod
    def calculate_late_fee(self, days_late):
        pass
    
    def checkout(self):
        self._is_available = False
    
    def return_item(self):
        self._is_available = True

class Book(LibraryItem):
    def __init__(self, title, author, year, item_id):
        super().__init__(title, author, year, item_id)
    def get_rental_period(self):
        return 14
    
    def calculate_late_fee(self, days_late):
        return days_late * 2

class EBook(LibraryItem):
    def __init__(self, title, author, year, item_id):
        super().__init__(title, author, year, item_id)
    def get_rental_period(self):
        return 7
    
    def calculate_late_fee(self, days_late):
        return days_late * 1

class AudioBook(LibraryItem):
    def __init__(self, title, author, year, item_id):
        super().__init__(title, author, year, item_id)
    def get_rental_period(self):
        return 21
    
    def calculate_late_fee(self, days_late):
        return days_late * 3

class Magazine(LibraryItem):
    def __init__(self, title, author, year, item_id, issue):
        super().__init__(title, author, year, item_id)
        self._issue = issue
    def get_rental_period(self):
        return 3
    
    def calculate_late_fee(self, days_late):
        return days_late * 5

class User(ABC):
    def __init__(self, first_name, last_name, user_id):
        self._first_name = first_name
        self._last_name = last_name
        self._user_id = user_id
        self._borrowed_items = []
        self._reservations = []

    @abstractmethod
    def get_max_items(self):
        pass

    @abstractmethod
    def get_rental_discount(self):
        pass

    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @property
    def user_id(self):
        return self._user_id

    @property
    def borrowed_items(self):
        return self._borrowed_items

    @property
    def reservations(self):
        return self._reservations

    def borrow_item(self, item):
        self._borrowed_items.append(item)
    
    def return_item(self, item):
        self._borrowed_items.remove(item)

    def reserve_item(self, item):
        self._reservations.append(item)

class Transaction:
    def __init__(self, user, item, checkout_date):
        self.user = user
        self.item = item
        self.checkout_date = checkout_date
        self.return_date = None
        self.fee = 0

class Student(User):
    def __init__(self, first_name, last_name, user_id):
        super().__init__(first_name, last_name, user_id)
    def get_max_items(self):
        return 5
    def get_rental_discount(self):
        return 0.5

class Employee(User):
    def __init__(self, first_name, last_name, user_id):
        super().__init__(first_name, last_name, user_id)
    def get_max_items(self):
        return 10
    def get_rental_discount(self):
        return 0.75

class Guest(User):
    def __init__(self, first_name, last_name, user_id):
        super().__init__(first_name, last_name, user_id)
    def get_max_items(self):
        return 2
    def get_rental_discount(self):
        return 0

class Library:
    def __init__(self,name):
        self._name = name
        self._items = {}
        self._users = {}
        self._transactions = []

    def add_item(self, item):
        self._items[item.item_id] = item

    def register_user(self, user):
        self._users[user.user_id] = user

    def process_checkout(self, user_id, item_id, checkout_date):
        if user_id not in self._users:
            raise InvalidUserError(f"Użytkownik {user_id} nie istnieje.")
        if item_id not in self._items:
            raise InvalidItemError(f"Przedmiot {item_id} nie istnieje.")

        user = self._users[user_id]
        item = self._items[item_id]

        if not item.is_available:
            raise ItemNotAvailableError(f"Przedmiot {item.title} jest już wypożyczony.")
        
        if len(user.borrowed_items) >= user.get_max_items():
            raise UserLimitExceededError(f"Użytkownik {user.first_name} przekroczył limit ({user.get_max_items()}).")

        transaction = Transaction(user, item, checkout_date)
        self._transactions.append(transaction)
        
        item.checkout()    
        user.borrow_item(item)

    def process_return(self, user_id, item_id, return_date):
        user = self._users.get(user_id)
        item = self._items.get(item_id)

        active_transaction = None
        for t in self._transactions:
            if t.user == user and t.item == item and t.return_date is None:
                active_transaction = t
                break

        if not active_transaction:
            raise Exception("Nie znaleziono aktywnego wypożyczenia dla tego duetu.")

        days_borrowed = (return_date - active_transaction.checkout_date).days
        allowed_days = item.get_rental_period()
        
        days_late = max(0, days_borrowed - allowed_days)
        
        base_fee = item.calculate_late_fee(days_late)
        discount = user.get_rental_discount()
        final_fee = base_fee * (1 - discount)

        active_transaction.return_date = return_date
        active_transaction.fee = final_fee
        
        item.return_item()
        user.return_item(item)
        
        print(f"Zwrot przyjęty. Opłata: {final_fee} zł.")


    def get_available_items(self):
        return [item for item in self._items.values() if item.is_available]

    def generate_report(self):
        print(f"\n--- RAPORT BIBLIOTEKI: {self._name} ---")
        for t in self._transactions:
            status = f"Zwrócono (Opłata: {t.fee} zł)" if t.return_date else "Wypożyczone"
            print(f"Użytkownik: {t.user.first_name} {t.user.last_name} | "
                  f"Pozycja: {t.item.title} | "
                  f"Status: {status}")


# Inicjalizacja biblioteki
library = Library("Biblioteka Główna")

# Dodawanie materiałów
book1 = Book("Python Fluent", "Luciano Ramalho", 2022, "B001")
ebook1 = EBook("Clean Code", "Robert Martin", 2008, "E001")
audiobook1 = AudioBook("Atomic Habits", "James Clear", 2018, "A001")
magazine1 = Magazine("Nature", "Various", 2024, "M001", issue=150)

library.add_item(book1)
library.add_item(ebook1)
library.add_item(audiobook1)
library.add_item(magazine1)

# Rejestracja użytkowników
student = Student("Jan", "Kowalski", "S001")
employee = Employee("Anna", "Nowak", "E001")
guest = Guest("Piotr", "Wiśniewski", "G001")

library.register_user(student)
library.register_user(employee)
library.register_user(guest)

# Wypożyczenia
from datetime import datetime, timedelta

checkout_date = datetime(2024, 11, 1)
library.process_checkout("S001", "B001", checkout_date)
library.process_checkout("E001", "E001", checkout_date)

# Zwroty z opóźnieniem
return_date = checkout_date + timedelta(days=20)  # 6 dni spóźnienia dla książki
library.process_return("S001", "B001", return_date)

# Wyświetl raport
library.generate_report()
