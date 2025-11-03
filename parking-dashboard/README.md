# 🚗 Parking Service API – Demo Setup & Usage

This project simulates a **smart parking garage system** with live API endpoints, terminal feedback, and a visual dashboard.  
It’s designed for **demo purposes and client presentations**.

---

## 📦 Project Structure

```
parking-dashboard/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── routers.py           # API route definitions
│   ├── services.py          # Business logic and cache
│   ├── VehicleType.py       # Enum for vehicle types
│   └── static/              # HTML dashboard with charts
├── simulate_apict.py        # Simulation script
└── README.md                # This file
```

---

## 🚀 How to Run the Demo

### 1. Start the backend server

```bash
uvicorn app.main:app --reload
```

- Runs FastAPI server at: [http://127.0.0.1:8000]
- Mounts dashboard (if present) at `/static`  
- Initializes cache and logs startup events  

---

### 2. Run the simulation script

```bash
python simulate_apict.py
```

- Simulates **vehicle entries and exits** with randomized data  
- Interacts with **API endpoints** to mimic real garage behavior  
- Displays **occupancy, active vehicles, and exit logs** in terminal  

---

## 📊 Visual Dashboard

Open in your browser:

```
http://127.0.0.1:8000/static/index.html
```

### Features
- 🟢 **Donut chart** – occupancy (free vs occupied)  
- 📊 **Bar chart** – daily revenue  
- 🚘 **Bar chart** – vehicle type distribution  
- 📋 **Live table** – active parked vehicles (auto-refresh every 10s)  

---

## 🔌 API Endpoints Overview

| Method | Endpoint                 | Description                               |
|--------|---------------------------|-------------------------------------------|
| POST   | `/vehicles/enter`        | Register vehicle entry, returns barcode    |
| POST   | `/vehicles/exit/{barcode}` | Process exit, calculate duration & revenue |
| GET    | `/occupancy`             | Show total capacity and current occupancy  |
| GET    | `/spaces/free`           | Return number of free parking spaces       |
| GET    | `/vehicles/active`       | List all currently parked vehicles         |
| GET    | `/revenue/today`         | Return total revenue for the current day   |
| GET    | `/health`                | Check service status                       |

---

## 🧪 Notes

- All data is **in-memory** and resets on server restart  
- Simulation generates **random Serbian-style license plates**  
- Dashboard **auto-refreshes every 10 seconds** for live feedback  

---

## 📄 License & Credits

This demo was developed by **Djordje Bogdanovic** for client presentation purposes.  
Feel free to adapt or extend for production use.  
