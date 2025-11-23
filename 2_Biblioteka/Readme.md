# Ćwiczenie: System Biblioteki Online

## Opis problemu
Zaprojektuj i zaimplementuj system biblioteki, który pozwala na:
- Zarządzanie różnymi typami materiałów (książki, e-booki, audiobooki, czasopisma)
- Rejestrację różnych typów użytkowników (studenci, pracownicy, goście)
- Wypożyczanie i zwracanie materiałów
- Naliczanie kar za przetrzymanie
- Rezerwację materiałów

## Wymagania funkcjonalne

### 1. Klasa abstrakcyjna `LibraryItem`
Bazowa klasa dla wszystkich materiałów w bibliotece:
- Atrybuty: tytuł, autor/twórca, rok wydania, unikalne ID, status dostępności
- Metody abstrakcyjne: `get_rental_period()`, `calculate_late_fee(days_late)`
- Metody konkretne: `checkout()`, `return_item()`

### 2. Klasy dziedziczące po `LibraryItem`
- `Book` - okres wypożyczenia: 14 dni, opłata: 2 zł/dzień
- `EBook` - okres wypożyczenia: 7 dni, opłata: 1 zł/dzień
- `AudioBook` - okres wypożyczenia: 21 dni, opłata: 3 zł/dzień
- `Magazine` - okres wypożyczenia: 3 dni, opłata: 5 zł/dzień

### 3. Klasa abstrakcyjna `User`
Bazowa klasa dla użytkowników:
- Atrybuty: imię, nazwisko, ID użytkownika, lista wypożyczonych pozycji, lista rezerwacji
- Metody abstrakcyjne: `get_max_items()`, `get_rental_discount()`
- Metody: `borrow_item()`, `return_item()`, `reserve_item()`

### 4. Klasy dziedziczące po `User`
- `Student` - max 5 pozycji, 50% zniżki na opłaty
- `Employee` - max 10 pozycji, 75% zniżki na opłaty
- `Guest` - max 2 pozycje, brak zniżki

### 5. Klasa `Library`
Zarządza całym systemem:
- Atrybuty: kolekcja materiałów, lista użytkowników, historia wypożyczeń
- Metody:
  - `add_item(item)`, `remove_item(item_id)`
  - `register_user(user)`, `remove_user(user_id)`
  - `process_checkout(user_id, item_id, date)`
  - `process_return(user_id, item_id, return_date)`
  - `get_available_items()`, `get_overdue_items()`
  - `generate_report()`

### 6. Obsługa wyjątków
Stwórz własne klasy wyjątków:
- `ItemNotAvailableError` - pozycja jest już wypożyczona
- `UserLimitExceededError` - użytkownik przekroczył limit wypożyczeń
- `InvalidItemError` - pozycja nie istnieje w systemie
- `InvalidUserError` - użytkownik nie jest zarejestrowany

## Dodatkowe wymagania

### Enkapsulacja
- Użyj właściwości prywatnych (konwencja `_attribute`)
- Zastosuj @property i @setter dla kontrolowanego dostępu do atrybutów

### Polimorfizm
- Implementuj wspólny interfejs dla różnych typów materiałów i użytkowników
- Użyj duck typing tam, gdzie to możliwe

### Klasa pomocnicza `Transaction`
- Przechowuje informacje o wypożyczeniu: użytkownik, pozycja, data wypożyczenia, data zwrotu, opłaty

## Przykładowy scenariusz testowy

```python
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
```
