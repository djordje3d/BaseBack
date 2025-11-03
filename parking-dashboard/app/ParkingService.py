from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Ticket, VehicleType, ParkingConfig
from app.VehicleType import VehicleType as VehicleTypeEnum

import datetime
import math
import uuid
import zlib
import random


class ParkingService:
    def __init__(self):
        self.db: Session = SessionLocal()
        config = self.db.query(ParkingConfig).first()
        self.capacity = config.capacity
        self.hourly_rate = config.default_rate

    def generate_bar_code(
        self, registration: str, vehicle_type: str, entry_time: datetime.datetime
    ) -> str:
        raw = (
            str(uuid.uuid4())
            + registration
            + vehicle_type
            + entry_time.strftime("%Y-%m-%d %H:%M:%S")
        )
        return format(zlib.crc32(raw.encode()), "08x")

    def get_free_spaces(self) -> int:
        active_count = self.db.query(Ticket).filter(Ticket.exit_time == None).count()
        return self.capacity - active_count

    def get_all_tickets(self):
        return self.db.query(Ticket).filter(Ticket.exit_time == None).all()

    def enter_vehicle(
        self, vehicle_registration: str, vehicle_type_enum: VehicleTypeEnum
    ):
        active_count = self.db.query(Ticket).filter(Ticket.exit_time == None).count()
        if active_count >= self.capacity:
            raise Exception("Parking is full")

        vehicle_type_obj = (
            self.db.query(VehicleType).filter_by(type=vehicle_type_enum.value).first()
        )
        if not vehicle_type_obj:
            raise Exception("Unknown vehicle type")

        random_hours = random.randint(1, 8)
        entry_time = datetime.datetime.now() - datetime.timedelta(hours=random_hours)
        bar_code = self.generate_bar_code(
            vehicle_registration, vehicle_type_enum.value, entry_time
        )

        ticket = Ticket(
            vehicle_registration=vehicle_registration,
            vehicle_type_id=vehicle_type_obj.id,
            entry_time=entry_time,
            bar_code=bar_code,
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        print(f"✅ Vehicle {vehicle_registration} entered ({random_hours}h ago).")
        return ticket

    def find_ticket_by_barcode(self, bar_code: str):
        return (
            self.db.query(Ticket).filter_by(bar_code=bar_code, exit_time=None).first()
        )

    def calculate_fee(self, ticket: Ticket) -> float:
        parked_duration = datetime.datetime.now() - ticket.entry_time
        hours_parked = math.ceil(parked_duration.total_seconds() / 3600)

        vehicle_type = (
            self.db.query(VehicleType).filter_by(id=ticket.vehicle_type_id).first()
        )
        rate = vehicle_type.rate if vehicle_type else self.hourly_rate
        return hours_parked * rate

    def exit_vehicle(self, ticket: Ticket) -> float:
        fee = self.calculate_fee(ticket)
        ticket.exit_time = datetime.datetime.now()
        ticket.fee = fee
        self.db.commit()
        print(f"🚗 Vehicle {ticket.vehicle_registration} exited. Fee: {fee} RSD.")
        return fee

    def show_parked_vehicles(self):
        tickets = self.get_all_tickets()
        if not tickets:
            print("🅿 Parking is empty.")
            return
        print(f"\n📋 Parked Vehicles: {len(tickets)}")
        print("-" * 60)
        for ticket in tickets:
            entry = ticket.entry_time.strftime("%d-%m-%Y %H:%M")
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            vehicle_type = (
                self.db.query(VehicleType).filter_by(id=ticket.vehicle_type_id).first()
            )
            print(
                f"Type: {vehicle_type.type:<5} | Reg: {ticket.vehicle_registration:<10} "
                f"| Entry: {entry} | Exit: {now} | Barcode: {ticket.bar_code}"
            )
        print("-" * 80)

    def show_occupancy_bar(self, bar_length=50):
        occupied = self.db.query(Ticket).filter(Ticket.exit_time == None).count()
        filled_blocks = math.floor((occupied / self.capacity) * bar_length)
        empty_blocks = bar_length - filled_blocks
        bar = "|" * filled_blocks + " " * empty_blocks
        print(f"\n📊 Occupancy: [{bar}] {occupied}/{self.capacity}\n")
