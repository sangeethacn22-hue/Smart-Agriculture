from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers and data store
from routes import (
    dashboard_router, 
    data_router, 
    ai_router, 
    analytics_router,
    data_store
)

app = FastAPI(
    title="Smart Agriculture API",
    description="API for Smart Agriculture Data Visualization Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3007", "http://127.0.0.1:3007"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

# Initialize with sample data
def initialize_sample_data():
    """Create sample data for quick demo"""
    
    # Crop data
    data_store["crops"] = [
        {"crop": "Rice", "region": "North", "season": "Kharif", "yield_tons": 3.5, "area_hectares": 1000, "year": 2023},
        {"crop": "Wheat", "region": "North", "season": "Rabi", "yield_tons": 4.2, "area_hectares": 800, "year": 2023},
        {"crop": "Cotton", "region": "South", "season": "Kharif", "yield_tons": 2.8, "area_hectares": 600, "year": 2023},
        {"crop": "Rice", "region": "South", "season": "Kharif", "yield_tons": 4.0, "area_hectares": 1200, "year": 2023},
        {"crop": "Maize", "region": "East", "season": "Kharif", "yield_tons": 3.2, "area_hectares": 500, "year": 2023},
        {"crop": "Wheat", "region": "West", "season": "Rabi", "yield_tons": 3.8, "area_hectares": 700, "year": 2023},
        {"crop": "Rice", "region": "North", "season": "Kharif", "yield_tons": 3.2, "area_hectares": 950, "year": 2022},
        {"crop": "Wheat", "region": "North", "season": "Rabi", "yield_tons": 4.0, "area_hectares": 780, "year": 2022},
    ]
    # Add to initialize_sample_data() in main.py
    data_store["weather"] = [
    {"region": "North", "month": "January", "temp_c": 15, "rainfall_mm": 20, "humidity": 65},
    # ... more data
]
    
    # Weather data
    data_store["weather"] = [
        {"region": "North", "month": "Jan", "temp_c": 15, "rainfall_mm": 20, "humidity": 65},
        {"region": "North", "month": "Feb", "temp_c": 18, "rainfall_mm": 25, "humidity": 60},
        {"region": "South", "month": "Jan", "temp_c": 28, "rainfall_mm": 50, "humidity": 75},
        {"region": "South", "month": "Feb", "temp_c": 30, "rainfall_mm": 45, "humidity": 73},
        {"region": "East", "month": "Jan", "temp_c": 20, "rainfall_mm": 80, "humidity": 80},
        {"region": "West", "month": "Jan", "temp_c": 22, "rainfall_mm": 15, "humidity": 55},
    ]
    
    # Soil health data
    data_store["soil"] = [
        {"region": "North", "ph": 7.2, "nitrogen": 280, "phosphorus": 25, "potassium": 210, "health": "Good"},
        {"region": "South", "ph": 6.8, "nitrogen": 310, "phosphorus": 30, "potassium": 240, "health": "Excellent"},
        {"region": "East", "ph": 6.5, "nitrogen": 260, "phosphorus": 22, "potassium": 190, "health": "Fair"},
        {"region": "West", "ph": 7.5, "nitrogen": 240, "phosphorus": 20, "potassium": 180, "health": "Fair"},
    ]
    
    # Yield trends
    data_store["yields"] = [
        {"year": 2021, "crop": "Rice", "yield_tons": 3.2, "region": "North"},
        {"year": 2022, "crop": "Rice", "yield_tons": 3.4, "region": "North"},
        {"year": 2023, "crop": "Rice", "yield_tons": 3.5, "region": "North"},
        {"year": 2021, "crop": "Wheat", "yield_tons": 3.8, "region": "North"},
        {"year": 2022, "crop": "Wheat", "yield_tons": 4.0, "region": "North"},
        {"year": 2023, "crop": "Wheat", "yield_tons": 4.2, "region": "North"},
    ]

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Smart Agriculture API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/api/dashboard/summary",
            "crops": "/api/data/crops",
            "weather": "/api/data/weather",
            "soil": "/api/data/soil",
            "advisory": "/api/ai/advisory",
            "analytics": "/api/analytics/regional-comparison"
        }
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00"}

# Initialize data on startup
@app.on_event("startup")
async def startup_event():
    initialize_sample_data()
    print("=" * 60)
    print("✅ Smart Agriculture API Started Successfully")
    print("=" * 60)
    print("📊 Sample data initialized")
    print("🌐 Server running on: http://localhost:8007")
    print("📖 API Documentation: http://localhost:8007/docs")
    print("=" * 60)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)