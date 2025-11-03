import datetime
import uuid
import math
import random

# Parking simulation
# Simulating vehicles entering the parking lot at random times
from enum import Enum
import zlib  # For generating bar codes


class VehicleType(Enum):
    CAR = 0
    BUS = 1
    TRUCK = 2


class Ticket:
    def __init__(self, vehicle_registration: str, vehicle_type: VehicleType):
        self.__id = uuid.uuid4()
        self.__entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__vehicle_registration = vehicle_registration
        self.__vehicle_type = vehicle_type
        self.__bar_code = self.generate_bar_code()

    def generate_bar_code(self) -> str:
        bar_code = (
            str(self.__id)
            + self.__vehicle_registration
            + self.__vehicle_type
            + self.__entry_time
        ).replace("-", "")
        return zlib.crc32(bar_code.encode()).hexdigest()

    # Getters
    def get_id(self) -> uuid.UUID:
        return self.__id

    def get_bar_code(self) -> str:
        return self.__bar_code

    def get_entry_time(self) -> str:
        return self.__entry_time

    def set_entry_time(self, new_time: str):
        """Used for simulation: set entry time to the past."""
        self.__entry_time = new_time

    def get_vehicle_registration(self) -> str:
        return self.__vehicle_registration

    def get_vehicle_type(self) -> VehicleType:
        return self.__vehicle_type


class ParkingService:
    def __init__(self, capacity=50, hourly_rate=120.0):
        self._capacity = capacity
        self._hourly_rate = hourly_rate  # Fallback rate
        self.__tickets = []

        # Vehicle-specific hourly rates
        self._vehicle_rates = {"car": 120.0, "bus": 200.0, "truck": 300.0}

    def get_free_spaces(self):
        return self._capacity - len(self.__tickets)

    def get_all_tickets(self):
        return list(self.__tickets)

    def enter_vehicle(self, vehicle_registration: str, vehicle_type: VehicleType):
        if len(self.__tickets) >= self._capacity:
            raise Exception("Parking is full")  # raise
        ticket = Ticket(vehicle_registration, vehicle_type)

        # Simulate random parking duration between 1 and 8 hours ago
        random_hours = random.randint(1, 8)
        fake_entry_time = datetime.datetime.now() - datetime.timedelta(
            hours=random_hours
        )
        ticket.set_entry_time(fake_entry_time)

        self.__tickets.append(ticket)
        print(
            f"✅ Vehicle {vehicle_registration} entered ({random_hours}h ago for simulation)."
        )
        return ticket

    def find_ticket_by_id(self, ticket_id):
        for ticket in self.__tickets:
            if ticket.get_id() == ticket_id:
                return ticket
        return None

    def find_ticket_by_barcode(self, bar_code):
        for ticket in self.__tickets:
            if ticket.get_bar_code() == bar_code:
                return ticket
        return None

    def calculate_fee(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if ticket:
            parked_duration = datetime.datetime.now() - ticket.get_entry_time()
            hours_parked = parked_duration.total_seconds() / 3600
            rate = self._vehicle_rates.get(ticket.get_vehicle_type(), self._hourly_rate)
            return (
                math.ceil(hours_parked) * rate
            )  # math.ceil funkcija služi za zaokruživanje na ceo broj
        return 0

    def exit_vehicle(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if ticket:
            fee = self.calculate_fee(ticket_id)
            self.__tickets.remove(ticket)
            print(
                f"🚗 Vehicle {ticket.get_vehicle_registration()} exited. Fee: {fee} RSD."
            )
            return fee
        return 0

    def show_parked_vehicles(self):
        if not self.__tickets:
            print("🅿 Parking is empty.")
            return
        countParkedVehicles = len(self.__tickets)
        print(f"\n📋 The number of Parked Vehicles: {countParkedVehicles}")
        print("-" * 60)
        for ticket in self.__tickets:
            time_str = ticket.get_entry_time().strftime("%d-%m-%Y-%H:%M")
            time_now_str = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
            print(
                f"Type: {ticket.get_vehicle_type()} | Reg: {ticket.get_vehicle_registration()} | Entry: {time_str} | Exit: {time_now_str} | Barcode: {ticket.get_bar_code()}"
            )
        print("-" * 60)  # Ispisuje crticu 60 puta

    def show_occupancy_bar(self, bar_length=50):
        occupied = len(self.__tickets)
        # free = self._capacity - occupied
        filled_blocks = math.floor((occupied / self._capacity) * bar_length)
        empty_blocks = bar_length - filled_blocks

        bar = "|" * filled_blocks + " " * empty_blocks
        print(
            f"\n📊 Parking occupancy (graphic): [{bar}] {occupied}/{self._capacity}\n"
        )

    @staticmethod
    def generate_registration(prefixes, suffixes):
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        number = random.randint(1000, 9999)
        return f"{prefix}{number}{suffix}"


# Example usage
if __name__ == "__main__":  # Main entry point for the simulation
    print("\n" + ("*" * 60))
    print("🚗 Parking Service Simulation Started")

    garage = ParkingService()
    garage.show_occupancy_bar()
    print(f"🅿️ FREE parking spaces: {garage.get_free_spaces()}\n")
    print("*" * 60)
    print("🅿️ Entering vehicles...")

    vehicle_prefixes = ["BG", "NS", "NI", "CA", "KG", "SU", "ZR", "VA"]
    vehicle_suffixes = ["JL", "UG", "HG", "SD", "ZH", "ED", "RT"]
    vehicle_types = [VehicleType.CAR, VehicleType.BUS, VehicleType.TRUCK]
    vehicle_count = random.randint(1, 10)  # nasumičan broj vozila

    for _ in range(vehicle_count):
        registration = garage.generate_registration(vehicle_prefixes, vehicle_suffixes)
        vehicle_type = random.choice(vehicle_types)
        garage.enter_vehicle(registration, vehicle_type)

    garage.show_parked_vehicles()
    garage.show_occupancy_bar()
    print(f"🅿️ FREE parking spaces: {garage.get_free_spaces()}\n")
    print("*" * 60)

    # Simulate exiting vehicles
    numberVehiclesExited = random.randint(1, 6)  # Random number of vehicles to exit
    for ticket in garage.get_all_tickets()[
        :numberVehiclesExited
    ]:  # Exit first two vehicles for simulation
        garage.exit_vehicle(ticket.get_id())

    garage.show_occupancy_bar()

    garage.show_parked_vehicles()
    print(f"🅿️ FREE parking spaces: {garage.get_free_spaces()}\n")
