from app.VehicleType import VehicleType
from app.Ticket import Ticket

import datetime
import math
import random


class ParkingService:
    def __init__(self, capacity=50, hourly_rate=120.0):
        self.capacity = capacity
        self.hourly_rate = hourly_rate
        self.tickets: list[Ticket] = []

        # Vehicle-specific rates
        self.vehicle_rates = {
            VehicleType.CAR: 120.0,
            VehicleType.BUS: 200.0,
            VehicleType.TRUCK: 300.0,
        }

    def get_free_spaces(self) -> int:
        return self.capacity - len(self.tickets)

    def get_all_tickets(self) -> list[Ticket]:
        return list(self.tickets)

    def enter_vehicle(self, vehicle_registration: str, vehicle_type: VehicleType):
        if len(self.tickets) >= self.capacity:
            raise Exception("Parking is full")

        ticket = Ticket(vehicle_registration, vehicle_type)

        # Simulate random parking duration between 1 and 8 hours ago
        random_hours = random.randint(1, 8)
        fake_entry_time = datetime.datetime.now() - datetime.timedelta(
            hours=random_hours
        )
        ticket.set_entry_time(fake_entry_time)

        self.tickets.append(ticket)
        print(f"✅ Vehicle {vehicle_registration} entered ({random_hours}h ago).")
        return ticket

    def find_ticket_by_barcode(self, bar_code):
        return next((t for t in self.tickets if t.bar_code == bar_code), None)

    def calculate_fee(self, ticket: Ticket) -> float:
        if not ticket:
            return 0.0
        parked_duration = datetime.datetime.now() - ticket.entry_time
        hours_parked = math.ceil(parked_duration.total_seconds() / 3600)
        rate = self.vehicle_rates.get(ticket.vehicle_type, self.hourly_rate)
        return hours_parked * rate

    def exit_vehicle(self, ticket: Ticket) -> float:
        if ticket not in self.tickets:
            raise Exception("Ticket not found")

        fee = self.calculate_fee(ticket)
        self.tickets.remove(ticket)
        print(f"🚗 Vehicle {ticket.vehicle_registration} exited. Fee: {fee} RSD.")
        return fee

    def show_parked_vehicles(self):
        if not self.tickets:
            print("🅿 Parking is empty.")
            return
        print(f"\n📋 Parked Vehicles: {len(self.tickets)}")
        print("-" * 60)
        for ticket in self.tickets:
            entry = ticket.entry_time.strftime("%d-%m-%Y %H:%M")
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            print(
                f"Type: {ticket.vehicle_type.name:<5} | Reg: {ticket.vehicle_registration:<10} "
                f"| Entry: {entry} | Exit: {now} | Barcode: {ticket.bar_code}"
            )
        print("-" * 80)

    def show_occupancy_bar(self, bar_length=50):
        occupied = len(self.tickets)
        filled_blocks = math.floor((occupied / self.capacity) * bar_length)
        empty_blocks = bar_length - filled_blocks
        bar = "|" * filled_blocks + " " * empty_blocks
        print(f"\n📊 Occupancy: [{bar}] {occupied}/{self.capacity}\n")
