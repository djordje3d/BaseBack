from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ParkingConfig(Base):
    __tablename__ = 'parking_config'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='parking_config_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    default_rate: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)


class Probnatabela(Base):
    __tablename__ = 'probnatabela'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='probnatabela_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    naziv: Mapped[Optional[str]] = mapped_column(String(30))


class VehicleTypes(Base):
    __tablename__ = 'vehicle_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vehicle_types_pkey'),
        UniqueConstraint('type', name='vehicle_types_type_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    rate: Mapped[decimal.Decimal] = mapped_column(Numeric, nullable=False)

    # Reverse relationship: one vehicle type → many tickets
    tickets: Mapped[list['Tickets']] = relationship('Tickets', back_populates='vehicle_type')


class Tickets(Base):
    __tablename__ = 'tickets'
    __table_args__ = (
        ForeignKeyConstraint(['vehicle_type_id'], ['vehicle_types.id'], name='tickets_vehicle_type_id_fkey'),
        PrimaryKeyConstraint('id', name='tickets_pkey'),
        UniqueConstraint('bar_code', name='tickets_bar_code_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vehicle_registration: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bar_code: Mapped[str] = mapped_column(String, nullable=False)
    entry_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    exit_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    status: Mapped[Optional[str]] = mapped_column(String)  # npr. 'ACTIVE', 'PAID', 'EXPIRED'

    # Relationship to VehicleType: many tickets → one vehicle type
    vehicle_type: Mapped['VehicleTypes'] = relationship('VehicleTypes', back_populates='tickets')
