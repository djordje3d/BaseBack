from sqlalchemy import Column, String, DateTime, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
import datetime

Base = declarative_base()  # Base class for declarative models. # SQLAlchemy ORM will use this to map classes to database tables.
# SQLAlchemy je kao DBContext u Entity Frameworku u .NET-u C#


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)  # e.g. 'CAR', 'BUS', 'TRUCK'
    rate = Column(Numeric, nullable=False)

    # Reverse relationship: one vehicle type → many tickets
    tickets = relationship("Ticket", back_populates="vehicle_type")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_registration = Column(String, nullable=False)
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=False)
    entry_time = Column(DateTime, default=datetime.datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    bar_code = Column(String, unique=True, nullable=False)
    fee = Column(Numeric, nullable=True)

    # Nova kolona
    status = Column(String, nullable=True)  # npr. 'ACTIVE', 'PAID', 'EXPIRED'

    # Relationship to VehicleType: many tickets → one vehicle type
    vehicle_type = relationship("VehicleType", back_populates="tickets")


class ParkingConfig(Base):
    __tablename__ = "parking_config"

    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)
    default_rate = Column(Numeric, nullable=False)
