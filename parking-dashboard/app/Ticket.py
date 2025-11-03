from app.VehicleType import VehicleType

import datetime
import uuid
import zlib


class Ticket:

    def __init__(self, vehicle_registration: str, vehicle_type: VehicleType):
        self.id = uuid.uuid4()
        self.entry_time = datetime.datetime.now()  # keep as datetime
        self.vehicle_registration = vehicle_registration
        self.vehicle_type = vehicle_type
        self.bar_code = self.generate_bar_code()

    def generate_bar_code(
        self,
    ) -> str:  # Generate a unique barcode based on ticket details
        bar_code = (
            str(self.id)
            + self.vehicle_registration
            + str(self.vehicle_type.value)
            + self.entry_time.strftime("%Y-%m-%d %H:%M:%S")  # Keep as string
        ).replace("-", "")
        return format(zlib.crc32(bar_code.encode()), "08x")  # Generate a hex string

    def set_entry_time(self, new_time: datetime.datetime):
        """Used for simulation: set entry time to the past."""
        self.entry_time = new_time
        self.bar_code = (
            self.generate_bar_code()
        )  # regenerate barcode due to time change

    def __repr__(self):  # String representation of the ticket
        return f"<Ticket {self.vehicle_registration} ({self.vehicle_type.name})>"
