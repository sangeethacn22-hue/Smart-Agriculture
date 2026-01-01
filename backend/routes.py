"""
API Routes for Smart Agriculture Platform
Separated routes for better organization
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional, List
import pandas as pd
from datetime import datetime
from models import (
    AdvisoryRequest, DashboardQuery, APIResponse,
    CropData, WeatherData, SoilData, YieldTrend
)
from service import AIService

# Create routers
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
data_router = APIRouter(prefix="/data", tags=["Data Management"])
ai_router = APIRouter(prefix="/ai", tags=["AI Services"])
analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Initialize AI service
ai_service = AIService()

# In-memory data store (in production, use a database)
data_store = {
    "crops": [],
    "weather": [],
    "soil": [],
    "yields": []
}


# ==================== Dashboard Routes ====================

@dashboard_router.get("/summary")
async def get_dashboard_summary(
    region: Optional[str] = Query(None, description="Filter by region"),
    season: Optional[str] = Query(None, description="Filter by season")
):
    """
    Get complete dashboard summary with all data
    """
    try:
        crops_data = data_store["crops"]
        
        # Apply filters if provided
        if region and region != "all":
            crops_data = [c for c in crops_data if c["region"] == region]
        if season and season != "all":
            crops_data = [c for c in crops_data if c["season"] == season]
        
        # Calculate statistics
        total_crops = len(set([c["crop"] for c in crops_data])) if crops_data else 0
        total_regions = len(set([c["region"] for c in crops_data])) if crops_data else 0
        avg_yield = (sum([c["yield_tons"] for c in crops_data]) / len(crops_data)) if crops_data else 0
        
        return {
            "total_crops": total_crops,
            "total_regions": total_regions,
            "average_yield": round(avg_yield, 2),
            "crops_data": crops_data,
            "weather_data": data_store["weather"],
            "soil_data": data_store["soil"],
            "yield_trends": data_store["yields"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@dashboard_router.get("/kpis")
async def get_kpis():
    """
    Get key performance indicators
    """
    try:
        crops_data = data_store["crops"]
        
        total_area = sum([c["area_hectares"] for c in crops_data])
        total_production = sum([c["yield_tons"] * c["area_hectares"] for c in crops_data])
        avg_productivity = total_production / total_area if total_area > 0 else 0
        
        return {
            "total_area_hectares": round(total_area, 2),
            "total_production_tons": round(total_production, 2),
            "average_productivity": round(avg_productivity, 2),
            "crop_diversity": len(set([c["crop"] for c in crops_data])),
            "active_regions": len(set([c["region"] for c in crops_data]))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Data Routes ====================

@data_router.get("/crops")
async def get_crops(
    region: Optional[str] = None,
    season: Optional[str] = None,
    crop: Optional[str] = None
):
    """
    Get crop data with optional filters
    """
    try:
        crops = data_store["crops"]
        
        if region:
            crops = [c for c in crops if c["region"] == region]
        if season:
            crops = [c for c in crops if c["season"] == season]
        if crop:
            crops = [c for c in crops if c["crop"] == crop]
        
        return {"crops": crops, "count": len(crops)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.post("/crops")
async def add_crop(crop_data: CropData):
    """
    Add new crop data
    """
    try:
        data_store["crops"].append(crop_data.dict())
        return {"message": "Crop data added successfully", "data": crop_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.get("/weather")
async def get_weather(region: Optional[str] = None):
    """
    Get weather data with optional region filter
    """
    try:
        weather = data_store["weather"]
        
        if region:
            weather = [w for w in weather if w["region"] == region]
        
        return {"weather": weather, "count": len(weather)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.post("/weather")
async def add_weather(weather_data: WeatherData):
    """
    Add new weather data
    """
    try:
        data_store["weather"].append(weather_data.dict())
        return {"message": "Weather data added successfully", "data": weather_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.get("/soil")
async def get_soil(region: Optional[str] = None):
    """
    Get soil health data with optional region filter
    """
    try:
        soil = data_store["soil"]
        
        if region:
            soil = [s for s in soil if s["region"] == region]
        
        return {"soil": soil, "count": len(soil)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.post("/soil")
async def add_soil(soil_data: SoilData):
    """
    Add new soil health data
    """
    try:
        data_store["soil"].append(soil_data.dict())
        return {"message": "Soil data added successfully", "data": soil_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.get("/yields")
async def get_yields(
    crop: Optional[str] = None,
    region: Optional[str] = None,
    year: Optional[int] = None
):
    """
    Get yield trend data with optional filters
    """
    try:
        yields = data_store["yields"]
        
        if crop:
            yields = [y for y in yields if y["crop"] == crop]
        if region:
            yields = [y for y in yields if y["region"] == region]
        if year:
            yields = [y for y in yields if y["year"] == year]
        
        return {"yields": yields, "count": len(yields)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@data_router.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """
    Upload CSV data file
    """
    try:
        # Read CSV file
        contents = await file.read()
        
        # Save to temporary location
        file_path = f"../data/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Try to parse CSV and add to data store
        try:
            df = pd.read_csv(file_path)
            data_type = file.filename.split('.')[0].lower()
            
            if data_type in data_store:
                data_store[data_type] = df.to_dict('records')
                return {
                    "message": f"File {file.filename} uploaded and processed successfully",
                    "records": len(df),
                    "data_type": data_type
                }
        except Exception as parse_error:
            return {
                "message": f"File {file.filename} uploaded but not parsed",
                "path": file_path,
                "note": "File saved but could not be automatically added to data store"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== AI Routes ====================

@ai_router.post("/advisory")
async def get_advisory(request: AdvisoryRequest):
    """
    Get AI-powered crop advisory
    """
    try:
        advisory = ai_service.get_crop_advisory(
            crop=request.crop,
            season=request.season,
            region=request.region
        )
        
        return {
            "crop": request.crop,
            "season": request.season,
            "region": request.region,
            "advisory": advisory,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ai_router.post("/risk-assessment")
async def assess_risk(
    crop: str,
    region: str,
    season: str
):
    """
    Assess agricultural risks
    """
    try:
        risks = ai_service.assess_risks(crop, region, season)
        return {
            "crop": crop,
            "region": region,
            "season": season,
            "risks": risks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ai_router.get("/recommendations/{crop}")
async def get_recommendations(
    crop: str,
    season: Optional[str] = None
):
    """
    Get best practices recommendations
    """
    try:
        recommendations = ai_service.get_recommendations(crop, season)
        return {
            "crop": crop,
            "season": season,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Analytics Routes ====================

@analytics_router.get("/regional-comparison")
async def regional_comparison(crop: Optional[str] = None):
    """
    Compare performance across regions
    """
    try:
        crops_data = data_store["crops"]
        
        if crop:
            crops_data = [c for c in crops_data if c["crop"] == crop]
        
        # Group by region
        regions = {}
        for crop_item in crops_data:
            region = crop_item["region"]
            if region not in regions:
                regions[region] = {
                    "region": region,
                    "total_yield": 0,
                    "total_area": 0,
                    "crop_count": 0
                }
            
            regions[region]["total_yield"] += crop_item["yield_tons"]
            regions[region]["total_area"] += crop_item["area_hectares"]
            regions[region]["crop_count"] += 1
        
        # Calculate averages
        for region in regions.values():
            region["average_yield"] = round(
                region["total_yield"] / region["crop_count"], 2
            ) if region["crop_count"] > 0 else 0
        
        return {"comparison": list(regions.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@analytics_router.get("/seasonal-trends")
async def seasonal_trends(region: Optional[str] = None):
    """
    Analyze seasonal trends
    """
    try:
        crops_data = data_store["crops"]
        
        if region:
            crops_data = [c for c in crops_data if c["region"] == region]
        
        # Group by season
        seasons = {}
        for crop in crops_data:
            season = crop["season"]
            if season not in seasons:
                seasons[season] = {
                    "season": season,
                    "total_production": 0,
                    "crop_types": set()
                }
            
            seasons[season]["total_production"] += crop["yield_tons"] * crop["area_hectares"]
            seasons[season]["crop_types"].add(crop["crop"])
        
        # Convert sets to counts
        for season in seasons.values():
            season["crop_diversity"] = len(season["crop_types"])
            season["crop_types"] = list(season["crop_types"])
        
        return {"trends": list(seasons.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@analytics_router.get("/yield-forecast")
async def yield_forecast(crop: str, region: str):
    """
    Simple yield forecast based on historical data
    """
    try:
        yields = data_store["yields"]
        
        # Filter by crop and region
        filtered = [
            y for y in yields 
            if y["crop"] == crop and y["region"] == region
        ]
        
        if not filtered:
            return {
                "message": "No historical data available for forecast",
                "crop": crop,
                "region": region
            }
        
        # Sort by year
        filtered.sort(key=lambda x: x["year"])
        
        # Simple linear trend
        if len(filtered) >= 2:
            years = [y["year"] for y in filtered]
            yields_vals = [y["yield_tons"] for y in filtered]
            
            # Calculate trend
            avg_change = (yields_vals[-1] - yields_vals[0]) / len(yields_vals)
            next_year = years[-1] + 1
            forecast = yields_vals[-1] + avg_change
            
            return {
                "crop": crop,
                "region": region,
                "historical_data": filtered,
                "forecast_year": next_year,
                "forecasted_yield": round(forecast, 2),
                "trend": "increasing" if avg_change > 0 else "decreasing"
            }
        
        return {
            "message": "Insufficient data for forecast",
            "crop": crop,
            "region": region,
            "data_points": len(filtered)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Export routers
__all__ = ['dashboard_router', 'data_router', 'ai_router', 'analytics_router', 'data_store']