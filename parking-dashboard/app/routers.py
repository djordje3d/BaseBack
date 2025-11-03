from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from app.VehicleType import VehicleType as VehicleTypeEnum
from app.services import service
from app.model import VehicleType, Ticket

router = APIRouter()


class VehicleEntry(BaseModel):
    registration: str
    vehicle_type: VehicleTypeEnum


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
def get_active_vehicles():
    tickets = service.get_all_tickets()
    result = []
    for t in tickets:
        vehicle_type_obj = (
            service.db.query(VehicleType).filter_by(id=t.vehicle_type_id).first()
        )
        result.append(
            {
                "type": vehicle_type_obj.type if vehicle_type_obj else "UNKNOWN",
                "registration": t.vehicle_registration,
                "entry_time": t.entry_time.strftime("%Y-%m-%d %H:%M"),
                "barcode": t.bar_code,
            }
        )
    return result


@router.get("/revenue/today")
def get_revenue_today():
    today = datetime.now().date()
    tickets_today = (
        service.db.query(Ticket)
        .filter(
            Ticket.entry_time >= datetime.combine(today, datetime.min.time()),
            Ticket.exit_time != None,
        )
        .all()
    )
    total = sum(service.calculate_fee(t) for t in tickets_today)
    return {"total_revenue": total}


@router.get("/health")
def healthcheck():
    return {"status": "ok", "timestamp": datetime.now().isoformat(), "version": "2.0.0"}
