# 🌾 Smart Agriculture Analytics Platform

A full-stack web application for agriculture data visualization and analysis, featuring an AI-powered crop advisory system, interactive dashboards, and comprehensive analytics tools for farmers and agriculture officers.

## Overview

This platform provides data-driven insights for agricultural decision-making through intuitive dashboards, weather analytics, crop performance tracking, and yield forecasting. Built with FastAPI backend and vanilla JavaScript frontend for optimal performance.

## Features

### Farmer Portal
- AI-powered crop advisory system with personalized recommendations
- Weather information and forecasting
- Crop performance tracking and analytics
- Risk assessment and mitigation strategies
- Season-specific cultivation guidelines

### Officer Dashboard
- Interactive data visualizations using Chart.js
- Regional performance comparison and analysis
- Seasonal trend tracking and reporting
- Yield forecasting based on historical data
- Soil health monitoring (NPK levels, pH)
- Export capabilities for reports
- Integrated Power BI dashboard for advanced analytics

### Power BI Integration
The platform includes a comprehensive Power BI dashboard that provides:
- Regional performance heatmaps and visualizations
- Multi-year trend analysis with interactive filtering
- Crop diversity metrics across regions
- Soil health scorecards and analysis
- Weather pattern correlations
- Custom KPI cards for quick insights

The Power BI dashboard is accessible through the officer portal (`powerbi.html`) and displays as an embedded PDF for easy viewing and sharing.

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Uvicorn - ASGI server
- Pandas - Data manipulation
- Pydantic - Data validation

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Chart.js - Data visualization
- Responsive design

**Analytics & Reporting:**
- Power BI Desktop - Advanced dashboard creation
- Rule-based advisory system
- Statistical analysis for forecasting

## Project Structure

```
smart-agriculture-platform/
│
├── backend/
│   ├── main.py              # Application entry point
│   ├── routes.py            # API endpoints
│   ├── models.py            # Data models
│   ├── service.py           # Advisory service logic
│   └── requirements.txt     # Dependencies
│
├── frontend/
│   ├── index.html          # Landing page
│   ├── farmer.html         # Farmer portal
│   ├── officer.html        # Officer dashboard
│   ├── powerbi.html        # Power BI viewer
│   ├── style.css           # Styles
│   ├── app.js              # Utilities
│   └── Agriculture_Dashboard.pdf
│
└── data/                   # CSV data storage
```

## Installation

### Prerequisites
- Python 3.8+
- Modern web browser
- pip package manager

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-agriculture-analytics-platform.git
cd smart-agriculture-analytics-platform
```

2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server
```bash
python main.py
```
Server runs on `http://localhost:8007`

4. Start the frontend server
```bash
cd frontend
python -m http.server 3007
```
Frontend available at `http://localhost:3007`

## Usage

### Accessing the Application
- Landing Page: `http://localhost:3007/index.html`
- Farmer Portal: `http://localhost:3007/farmer.html`
- Officer Dashboard: `http://localhost:3007/officer.html`
- Power BI Dashboard: `http://localhost:3007/powerbi.html`
- API Documentation: `http://localhost:8007/docs`

### API Endpoints

**Dashboard**
```
GET  /api/dashboard/summary       # Complete dashboard data
GET  /api/dashboard/kpis          # Key performance indicators
```

**Data Management**
```
GET  /api/data/crops              # Retrieve crop data
POST /api/data/crops              # Add crop records
GET  /api/data/weather            # Get weather data
POST /api/data/weather            # Add weather records
GET  /api/data/soil               # Get soil health data
POST /api/data/soil               # Add soil records
POST /api/data/upload             # Upload CSV files
```

**AI Services**
```
POST /api/ai/advisory             # Get crop advisory
POST /api/ai/risk-assessment      # Assess risks
GET  /api/ai/recommendations/{crop} # Get best practices
```

**Analytics**
```
GET /api/analytics/regional-comparison  # Compare regions
GET /api/analytics/seasonal-trends      # Analyze trends
GET /api/analytics/yield-forecast       # Forecast yields
```

## Advisory System

The AI advisory system provides recommendations for multiple crops including:
- Rice (Kharif & Rabi)
- Wheat (Rabi)
- Cotton (Kharif)
- Maize (Kharif & Rabi)
- Sugarcane, Pulses, Vegetables

Each advisory includes:
- Trend analysis
- Cultivation recommendations
- Risk identification
- Mitigation strategies
- Regional adjustments

## Power BI Dashboard

### Creating/Updating the Dashboard

1. Open Power BI Desktop
2. Connect to your data sources or import CSV files
3. Create visualizations (charts, tables, KPIs)
4. Design the layout and apply themes
5. Export as PDF: File → Export → Export to PDF
6. Save as `Agriculture_Dashboard.pdf` in the frontend directory

### Viewing the Dashboard

The Power BI dashboard is embedded in the web application and can be accessed through the officer portal. Features include:
- Zoom and pan controls
- Print functionality
- Download capability
- Fullscreen mode
- Direct link sharing

## Sample Data

The application includes sample data:
- 8 crop records (various regions and seasons)
- 6 weather data points
- 4 soil health assessments
- 6 yield trend records (2021-2023)

## Configuration

Backend configuration in `main.py`:
```python
API_BASE = 'http://localhost:8007/api'
BACKEND_PORT = 8007
```

Frontend configuration in `app.js`:
```javascript
const CONFIG = {
    API_BASE: 'http://localhost:8006/api',
    FRONTEND_PORT: 3007,
    BACKEND_PORT: 8006
};
```

## Data Models

Key data models include:
- `CropData` - Crop information and yields
- `WeatherData` - Temperature, rainfall, humidity
- `SoilData` - NPK levels and pH
- `YieldTrend` - Historical yield data
- `AdvisoryRequest` - Advisory input parameters
- `AdvisoryResponse` - Generated recommendations

## Error Handling

The application includes:
- Input validation using Pydantic
- CORS middleware for secure requests
- Try-catch blocks for API calls
- User-friendly error messages
- Loading states and indicators

