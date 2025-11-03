from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.ParkingService import ParkingService

service = ParkingService()

# Konfiguriši keš (InMemory sa default TTL=300s)


def init_cache(app):

    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
