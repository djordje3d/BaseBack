from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.database import init_db

from app.routers import router
from app.services import init_cache

app = FastAPI()

# Uključi API rute
app.include_router(router)

print("✅ Registered routes:")
for route in app.routes:
    print(f"  {route.path} -> {route.name}")

# Proveri da li postoji statički folder pre montiranja
static_path = Path("app/static")

if static_path.exists() and static_path.is_dir():  # Provera da li je folder pronađen
    print("📁 Static folder found — mounting at /static")
    app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

else:
    print("⚠️ Static folder not found — skipping mount")

# Inicijalizacija keša pri pokretanju


@app.on_event("startup")  # Dodato za inicijalizaciju keša
def on_startup():
    print("🚀 Startup event triggered")
    # init_cache(app)


@app.on_event("startup")  # Dodato za inicijalizaciju baze podataka
def startup():
    init_db()


# This ensures your tables are created if they don’t exist — useful during development before switching to Alembic migrations.
