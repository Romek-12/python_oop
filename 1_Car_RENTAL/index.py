from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, model, price_per_day):
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
    def __str__(self):
        return f"{self.brand} {self.model} - {self.price_per_day} PLN/dzień"

class Car(Vehicle):
    pass
class Bike(Vehicle):
    pass
class Scooter(Vehicle):
    pass


class Rental:
    def __init__(self, vehicle, days):
        self.vehicle = vehicle
        self.days = days

class Rental_Service:
    def __init__(self):
        self.vehicles = []
        self.rentals = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle) 

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)

    def rent_vehicle(self, vehicle, days):
        new_rental = Rental(vehicle, days)
        self.rentals.append(new_rental)
        return new_rental   

    def return_vehicle(self, rental):
        self.rentals.remove(rental)

moje_biuro = Rental_Service()

auto1 = Car("Toyota", "Corolla", 60)
auto2 = Car("Renault", "Clio 2025", 45)
auto3 = Car("Ferrari", "296 GTS", 350)

moje_biuro.add_vehicle(auto1)
moje_biuro.add_vehicle(auto2)
moje_biuro.add_vehicle(auto3)

print("Dostępne pojazdy:")
for p in moje_biuro.vehicles:
    print(p)

print("\nWypożyczam Ferrari na 6 dni")
wynajem = moje_biuro.rent_vehicle(auto3, 6)
print(f"Wynajęty samochód: {wynajem.vehicle.brand} na {wynajem.days} dni")

print(f"Ilość aktywnych wynajmów: {len(moje_biuro.rentals)}")

