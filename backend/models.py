"""
Data models for Smart Agriculture Platform
Using Pydantic for data validation
"""

from ast import pattern
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class Season(str, Enum):
    KHARIF = "Kharif"
    RABI = "Rabi"
    ZAID = "Zaid"


class Region(str, Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    CENTRAL = "Central"


class SoilHealth(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"


# Request Models
class AdvisoryRequest(BaseModel):
    """Request model for AI advisory"""
    crop: str = Field(..., min_length=2, max_length=50, description="Crop name")
    season: str = Field(..., description="Growing season")
    region: Optional[str] = Field(default="General", description="Geographic region")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop": "Rice",
                "season": "Kharif",
                "region": "North"
            }
        }


class DashboardQuery(BaseModel):
    """Query parameters for dashboard data"""
    region: Optional[str] = None
    crop: Optional[str] = None
    season: Optional[str] = None
    year: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "region": "North",
                "crop": "Rice",
                "season": "Kharif",
                "year": 2023
            }
        }


class DataUploadRequest(BaseModel):
    """Request model for data upload"""
    data_type: str = Field(..., description="Type of data (crops, weather, soil)")
    data: List[Dict[str, Any]] = Field(..., description="Data records")


# Response Models
class CropData(BaseModel):
    """Crop data model"""
    crop: str
    region: str
    season: str
    yield_tons: float = Field(..., ge=0, description="Yield in tons")
    area_hectares: float = Field(..., ge=0, description="Area in hectares")
    year: Optional[int] = None
    
    @validator('yield_tons', 'area_hectares')
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError('Value must be positive')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "crop": "Rice",
                "region": "North",
                "season": "Kharif",
                "yield_tons": 3.5,
                "area_hectares": 1000,
                "year": 2023
            }
        }


class WeatherData(BaseModel):
    """Weather data model"""
    region: str
    month: str
    temp_c: float = Field(..., description="Temperature in Celsius")
    rainfall_mm: float = Field(..., ge=0, description="Rainfall in mm")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    
    @validator('humidity')
    def validate_humidity(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Humidity must be between 0 and 100')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "region": "North",
                "month": "January",
                "temp_c": 15.5,
                "rainfall_mm": 20.0,
                "humidity": 65
            }
        }


class SoilData(BaseModel):
    """Soil health data model"""
    region: str
    ph: float = Field(..., ge=0, le=14, description="Soil pH level")
    nitrogen: float = Field(..., ge=0, description="Nitrogen content in kg/ha")
    phosphorus: float = Field(..., ge=0, description="Phosphorus content in kg/ha")
    potassium: float = Field(..., ge=0, description="Potassium content in kg/ha")
    organic_carbon: Optional[float] = Field(None, ge=0, description="Organic carbon percentage")
    health: str = Field(..., description="Overall soil health status")
    
    @validator('ph')
    def validate_ph(cls, v):
        if not 0 <= v <= 14:
            raise ValueError('pH must be between 0 and 14')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "region": "North",
                "ph": 7.2,
                "nitrogen": 280,
                "phosphorus": 25,
                "potassium": 210,
                "organic_carbon": 0.65,
                "health": "Good"
            }
        }


class YieldTrend(BaseModel):
    """Yield trend data model"""
    year: int = Field(..., ge=2000, le=2100)
    crop: str
    yield_tons: float = Field(..., ge=0)
    region: str
    
    class Config:
        schema_extra = {
            "example": {
                "year": 2023,
                "crop": "Rice",
                "yield_tons": 3.5,
                "region": "North"
            }
        }


class AdvisoryResponse(BaseModel):
    """Response model for AI advisory"""
    crop: str
    season: str
    region: str
    advisory: Dict[str, str] = Field(..., description="Advisory details")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "crop": "Rice",
                "season": "Kharif",
                "region": "North",
                "advisory": {
                    "trend": "Rice yields are stable in Kharif season",
                    "advisory": "Ensure proper water management",
                    "risks": "Monitor for pest attacks",
                    "recommendations": "Use certified seeds"
                },
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class DashboardSummary(BaseModel):
    """Dashboard summary response"""
    total_crops: int
    total_regions: int
    average_yield: float
    crops_data: List[Dict[str, Any]]
    weather_data: List[Dict[str, Any]]
    soil_data: List[Dict[str, Any]]
    yield_trends: List[Dict[str, Any]]
    
    class Config:
        schema_extra = {
            "example": {
                "total_crops": 5,
                "total_regions": 4,
                "average_yield": 3.5,
                "crops_data": [],
                "weather_data": [],
                "soil_data": [],
                "yield_trends": []
            }
        }


class APIResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {},
                "error": None
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Not Found",
                "detail": "Resource not found",
                "status_code": 404,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


# Statistics Models
class RegionStatistics(BaseModel):
    """Statistics for a region"""
    region: str
    total_area: float
    total_production: float
    average_yield: float
    crop_count: int
    dominant_crop: Optional[str] = None


class CropStatistics(BaseModel):
    """Statistics for a crop"""
    crop: str
    total_area: float
    total_production: float
    average_yield: float
    region_count: int
    best_performing_region: Optional[str] = None


class SeasonalComparison(BaseModel):
    """Seasonal comparison data"""
    season: str
    total_production: float
    average_yield: float
    crop_diversity: int


# User Models (for future authentication)
class User(BaseModel):
    """User model"""
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: str = Field(default="farmer", description="User role: farmer or officer")
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "farmer_john",
                "email": "john@example.com",
                "role": "farmer",
                "is_active": True
            }
        }


class UserCreate(BaseModel):
    """User creation model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)
    role: str = Field(default="farmer")


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str


# Validation helpers
def validate_crop_name(crop: str) -> str:
    """Validate and normalize crop name"""
    crop = crop.strip().title()
    valid_crops = ["Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Pulses", "Oilseeds"]
    if crop not in valid_crops:
        # Allow custom crops but log warning
        pass
    return crop


def validate_season(season: str) -> str:
    """Validate season name"""
    season = season.strip().title()
    valid_seasons = ["Kharif", "Rabi", "Zaid"]
    if season not in valid_seasons:
        raise ValueError(f"Season must be one of: {', '.join(valid_seasons)}")
    return season


def validate_region(region: str) -> str:
    """Validate region name"""
    region = region.strip().title()
    valid_regions = ["North", "South", "East", "West", "Central"]
    if region not in valid_regions and region != "General":
        raise ValueError(f"Region must be one of: {', '.join(valid_regions)}")
    return region