from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from datetime import datetime
from app.VehicleType import VehicleType
from pydantic import BaseModel
import random

from app.services import service

router = APIRouter()


class VehicleEntry(BaseModel):
    registration: str
    vehicle_type: VehicleType


@router.post("/vehicles/enter")
def enter_vehicle(data: VehicleEntry):
    ticket = service.enter_vehicle(data.registration, data.vehicle_type)
    return {
        "message": "Vehicle entered",
        "barcode": ticket.bar_code,
        "entry_time": ticket.entry_time.strftime("%Y-%m-%d %H:%M"),
    }


@router.post("/vehicles/exit/{barcode}")
def exit_vehicle(barcode: str):
    ticket = service.find_ticket_by_barcode(barcode)
    if not ticket:
        return {"error": "Ticket not found"}
    fee = service.exit_vehicle(ticket)
    return {
        "message": "Vehicle exited",
        "Reg": ticket.vehicle_registration,
        "fee": fee,
    }


@router.get("/spaces/free")
def get_free_spaces():
    return {"free_spaces": service.get_free_spaces()}


@router.get("/occupancy")
def get_occupancy():
    occupied = service.capacity - service.get_free_spaces()
    percent = occupied / service.capacity * 100
    return {"capacity": service.capacity, "percent": percent}


@router.get("/vehicles/active")
# @cache(expire=60)  # Disable caching for real-time data
def get_active_vehicles():
    tickets = service.get_all_tickets()
    return [
        {
            "type": t.vehicle_type.name,
            "registration": t.vehicle_registration,
            "entry_time": t.entry_time.strftime("%Y-%m-%d %H:%M"),
            "barcode": t.bar_code,
        }
        for t in tickets
    ]


@router.get("/revenue/today")
def get_revenue_today():
    today = datetime.now().date()
    total = sum(
        service.calculate_fee(t)
        for t in service.tickets
        if t.entry_time.date() == today
    )
    return {"total_revenue": total}


@router.get("/health")
def healthcheck():
    return {"status": "ok", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}
