import random

# Vehicle types for parking

from ParkingService import ParkingService
from VehicleType import VehicleType

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
        vehicle_type = random.choice(vehicle_types)  # "choice" je random funkcija iz enuma VehicleType
        garage.enter_vehicle(registration, vehicle_type)

    garage.show_parked_vehicles()
    garage.show_occupancy_bar()
    print(f"🅿️ FREE parking spaces: {garage.get_free_spaces()}\n")
    print("*" * 60)

    # Simulate exiting vehicles
    numberVehiclesExited = random.randint(1, 6)  # Random number of vehicles to exit
    for ticket in garage.get_all_tickets()[
        :numberVehiclesExited
    ]:
        garage.exit_vehicle(ticket)

    garage.show_occupancy_bar()  # Show occupancy after vehicles exit

    garage.show_parked_vehicles()
    print(f"🅿️ FREE parking spaces: {garage.get_free_spaces()}\n")
