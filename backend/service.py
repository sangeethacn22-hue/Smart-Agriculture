"""
AI Service for Smart Agriculture Platform
Rule-based advisory system (no API key required)
Can be extended with OpenAI/Claude API later
"""

from typing import Dict, List, Optional
from datetime import datetime
import random


class AIService:
    """
    AI Service for generating crop advisories and recommendations
    Uses rule-based system with agricultural knowledge base
    """
    
    def __init__(self):
        """Initialize AI service with knowledge base"""
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict:
        """
        Initialize comprehensive agricultural knowledge base
        """
        return {
            "rice": {
                "kharif": {
                    "trend": "Rice yields in Kharif season show stable performance with good monsoon patterns. Historical data indicates 3.2-4.0 tons/ha average yield.",
                    "advisory": "Ensure proper water management with 2-3 cm standing water during critical growth stages. Apply nitrogen fertilizer in 3 splits: 50% basal, 25% at tillering, 25% at panicle initiation. Maintain field drainage during heavy rainfall periods.",
                    "risks": "Primary risks include brown plant hopper infestation, stem borer attacks, and blast disease. Monitor for bacterial leaf blight in high humidity. Flash floods can damage crops in low-lying areas.",
                    "recommendations": "Use certified seed varieties (rate: 20-25 kg/acre). Apply zinc sulfate if deficiency symptoms appear. Implement integrated pest management (IPM) with pheromone traps. Spray fungicides preventively for blast control in endemic areas."
                },
                "rabi": {
                    "trend": "Rabi rice requires supplemental irrigation and shows moderate yield potential (2.5-3.5 tons/ha). Performance depends on irrigation availability.",
                    "advisory": "Maintain 2-3 cm standing water throughout growth period. Apply urea at tillering stage (3-4 weeks after transplanting). Monitor temperature closely as cold stress can affect crop.",
                    "risks": "Cold temperature stress during reproductive stage. Bacterial leaf blight in humid conditions. Water stress if irrigation is inadequate.",
                    "recommendations": "Use short-duration varieties (100-110 days). Ensure timely transplanting (mid-November). Apply potash to improve cold tolerance. Implement proper weed management in first 30 days."
                }
            },
            "wheat": {
                "rabi": {
                    "trend": "Wheat performs excellently in Rabi season with optimal temperature ranges. Average yields of 4.0-5.0 tons/ha achievable with good management.",
                    "advisory": "Sow between mid-November to early December for optimal results. Apply NPK fertilizers as per soil test: typically 120:60:40 kg/ha. First irrigation critical at crown root stage (21 days after sowing).",
                    "risks": "Yellow rust (stripe rust) in high humidity and moderate temperatures. Aphid infestation during grain filling. Terminal heat stress if sowing delayed.",
                    "recommendations": "Use resistant varieties for rust-prone areas. Apply first irrigation at 21 days (CRI stage). Follow up with irrigations at tillering, jointing, flowering, and milk stages. Monitor for aphids and spray if threshold exceeded."
                },
                "kharif": {
                    "trend": "Wheat is not recommended for Kharif season due to high temperatures and humidity which are unfavorable for growth.",
                    "advisory": "Wheat cultivation is not advisable during Kharif season. Consider alternative crops like maize, sorghum, or pearl millet.",
                    "risks": "Complete crop failure likely due to unsuitable climatic conditions. High disease pressure from moisture and heat.",
                    "recommendations": "Switch to Kharif-suitable crops. If attempting in hill regions with cooler climate, use special varieties and ensure disease management."
                }
            },
            "cotton": {
                "kharif": {
                    "trend": "Cotton is a major Kharif crop with yields ranging from 2.5-3.5 tons/ha lint. Performance heavily dependent on pest management and rainfall distribution.",
                    "advisory": "Maintain plant spacing of 60x30 cm for optimal growth. Regular scouting for pests essential - check crops twice weekly. Apply nitrogen in splits: 25% at sowing, 50% at square formation, 25% at flowering.",
                    "risks": "Bollworm complex (American, spotted, pink) is major threat. Whitefly and jassids cause significant damage. Pink bollworm particularly destructive in late season.",
                    "recommendations": "Use Bt cotton hybrids for bollworm resistance. Install pheromone traps (8-10 per acre). Practice crop rotation to break pest cycles. Avoid excessive nitrogen which attracts pests. Remove and destroy crop residues after harvest."
                },
                "rabi": {
                    "trend": "Cotton can be grown in southern regions during Rabi with irrigation, but yields are generally lower (2.0-2.5 tons/ha).",
                    "advisory": "Requires assured irrigation throughout growth period. Monitor for pest buildup which can be higher in dry conditions.",
                    "risks": "Water stress without adequate irrigation. Pest pressure can be severe in dry conditions. Pink bollworm particularly problematic.",
                    "recommendations": "Use early-maturing varieties. Ensure drip irrigation if possible for water efficiency. Intensive pest monitoring required."
                }
            },
            "maize": {
                "kharif": {
                    "trend": "Maize is a high-yielding Kharif crop with potential of 6-8 tons/ha under good management. Well-suited to monsoon conditions.",
                    "advisory": "Plant at 60x20 cm spacing for optimal population density. Apply nitrogen at V6 stage (6-leaf stage) for maximum efficiency. Ensure weed control in first 30-35 days which is critical period.",
                    "risks": "Fall armyworm is emerging as major threat - can cause 20-50% yield loss. Stem borer during vegetative stage. Lodging in high winds if plant population excessive.",
                    "recommendations": "Use hybrid seeds for better yield and uniformity. Apply pre-emergence herbicide followed by one hand weeding. Scout for fall armyworm weekly. Apply recommended insecticides if 5% plants show damage. Ensure adequate potassium for stem strength."
                },
                "rabi": {
                    "trend": "Rabi maize shows good potential with irrigation, especially in southern and western regions. Yields of 5-7 tons/ha achievable.",
                    "advisory": "Sow early (mid-October to November) to avoid terminal heat stress. Irrigation critical during flowering and grain filling stages.",
                    "risks": "Aphids and corn leaf aphids during cooler period. Termite damage in dry conditions. Heat stress if maturity coincides with summer.",
                    "recommendations": "Use short to medium duration hybrids (90-100 days). Apply 4-5 irrigations at critical stages. Monitor for aphids and spray if needed."
                }
            },
            "sugarcane": {
                "kharif": {
                    "trend": "Sugarcane is a long-duration crop (10-12 months) planted during Kharif. Yields of 80-100 tons/ha achievable with good practices.",
                    "advisory": "Use 3-budded setts for planting. Maintain row spacing of 90-120 cm. Apply high doses of organic manure (25 tons/ha) along with chemical fertilizers. Earthing up essential at 90-120 days.",
                    "risks": "Early shoot borer during establishment. Top borer and internode borer during growth. Red rot disease in susceptible varieties. Waterlogging can cause root damage.",
                    "recommendations": "Use disease-resistant varieties. Treat setts with fungicide before planting. Implement drip irrigation with fertigation for better efficiency. Practice trash mulching to conserve moisture and suppress weeds."
                }
            },
            "pulses": {
                "kharif": {
                    "trend": "Kharif pulses (arhar, moong, urad) are important for soil health and nutrition. Average yields 1.0-1.5 tons/ha.",
                    "advisory": "Minimal fertilizer requirement due to nitrogen fixation. Apply only phosphorus (40-60 kg/ha) and potash. Seed treatment with Rhizobium culture improves nodulation.",
                    "risks": "Pod borer complex causes major yield loss. Waterlogging highly detrimental. Diseases like yellow mosaic virus and powdery mildew.",
                    "recommendations": "Use certified disease-resistant varieties. Practice timely sowing. Install bird perches for biological pest control. Spray neem-based pesticides for eco-friendly management."
                },
                "rabi": {
                    "trend": "Rabi pulses (gram, lentil, pea) show good performance in cooler temperatures. Important for crop rotation and soil fertility.",
                    "advisory": "Sow at optimal time (October-November) to avoid terminal heat. Minimal irrigation required (1-2 irrigations). Light fertilizer application sufficient.",
                    "risks": "Gram pod borer in chickpea. Wilt and root rot diseases. Aphids during flowering period.",
                    "recommendations": "Use wilt-resistant varieties in affected areas. One irrigation at flowering critical for yield. Harvest at right maturity to prevent shattering."
                }
            },
            "vegetables": {
                "kharif": {
                    "trend": "Kharif vegetables include tomato, brinjal, okra, bottle gourd. Require intensive management but offer high returns.",
                    "advisory": "Use raised beds for drainage. Apply organic manure heavily (20-30 tons/ha). Drip irrigation with plastic mulch improves efficiency and quality.",
                    "risks": "High disease and pest pressure due to humid conditions. Viral diseases transmitted by whitefly and aphids. Fruit flies in cucurbits.",
                    "recommendations": "Use resistant hybrids. Implement protected cultivation for high-value crops. Regular monitoring and timely pesticide application. Ensure proper drainage to prevent root diseases."
                },
                "rabi": {
                    "trend": "Rabi vegetables show excellent quality with lower pest pressure. Include cabbage, cauliflower, tomato, peas.",
                    "advisory": "Optimal growth conditions due to cooler temperature. Irrigation more frequent as moisture stress affects quality.",
                    "risks": "Aphids and caterpillar pests. Frost damage in extreme north. Premature bolting in leafy vegetables if temperature rises.",
                    "recommendations": "Use appropriate varieties for the season. Apply micronutrients for better quality. Harvest at optimal maturity for best market price."
                }
            }
        }
    
    def get_crop_advisory(self, crop: str, season: str, region: str = "General") -> Dict[str, str]:
        """
        Get comprehensive crop advisory based on crop, season, and region
        
        Args:
            crop: Crop name (e.g., "Rice", "Wheat")
            season: Growing season (e.g., "Kharif", "Rabi")
            region: Geographic region
        
        Returns:
            Dictionary with trend, advisory, risks, and recommendations
        """
        crop = crop.lower()
        season = season.lower()
        
        # Get base advisory from knowledge base
        if crop in self.knowledge_base:
            if season in self.knowledge_base[crop]:
                advisory = self.knowledge_base[crop][season].copy()
                
                # Add region-specific modifications
                advisory = self._add_regional_context(advisory, region)
                
                # Add current date context
                advisory["generated_date"] = datetime.now().strftime("%Y-%m-%d")
                
                return advisory
        
        # Default advisory if crop/season not in knowledge base
        return self._generate_default_advisory(crop, season, region)
    
    def _add_regional_context(self, advisory: Dict[str, str], region: str) -> Dict[str, str]:
        """Add region-specific context to advisory"""
        
        regional_notes = {
            "North": "In northern regions, consider frost protection during winter months. Cold temperatures can stress crops.",
            "South": "Southern regions benefit from higher temperatures but require careful water management during dry periods.",
            "East": "Eastern regions receive good rainfall but may face flooding. Ensure proper drainage systems.",
            "West": "Western regions often face water scarcity. Implement efficient irrigation methods like drip or sprinkler.",
            "Central": "Central regions have diverse conditions. Adapt practices based on local microclimate."
        }
        
        if region in regional_notes:
            advisory["regional_note"] = regional_notes[region]
        
        return advisory
    
    def _generate_default_advisory(self, crop: str, season: str, region: str) -> Dict[str, str]:
        """Generate default advisory for crops not in knowledge base"""
        
        return {
            "trend": f"{crop.title()} cultivation in {season.title()} season shows variable performance depending on local conditions and management practices.",
            "advisory": f"Follow local agricultural guidelines for {crop} cultivation. Conduct soil testing before planting to determine nutrient requirements. Ensure proper seed selection and treatment.",
            "risks": "Monitor regularly for pest and disease issues. Weather extremes can affect crop performance. Consult local agriculture department for region-specific risks.",
            "recommendations": f"Use certified seeds. Follow recommended spacing and planting density. Implement integrated pest management. Maintain proper irrigation schedule. Consult local agriculture extension officers for specific guidance on {crop} cultivation.",
            "note": "This is a general advisory. For detailed crop-specific recommendations, please consult your local agriculture department.",
            "generated_date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def assess_risks(self, crop: str, region: str, season: str) -> List[Dict[str, str]]:
        """
        Assess specific risks for crop-region-season combination
        
        Returns:
            List of risk assessments with severity and mitigation
        """
        crop = crop.lower()
        season = season.lower()
        
        # Common risks database
        risks = []
        
        # Weather-based risks
        if season == "kharif":
            risks.append({
                "type": "Weather",
                "risk": "Heavy rainfall and flooding",
                "severity": "High",
                "probability": "Medium",
                "mitigation": "Ensure proper drainage systems. Plant on raised beds in flood-prone areas."
            })
            risks.append({
                "type": "Pest",
                "risk": "Increased pest pressure due to humidity",
                "severity": "High",
                "probability": "High",
                "mitigation": "Regular monitoring. Implement IPM practices. Use pheromone traps."
            })
        elif season == "rabi":
            risks.append({
                "type": "Weather",
                "risk": "Cold stress and frost damage",
                "severity": "Medium",
                "probability": "Medium",
                "mitigation": "Use cold-tolerant varieties. Apply light irrigation during frost nights."
            })
            risks.append({
                "type": "Water",
                "risk": "Irrigation water scarcity",
                "severity": "Medium",
                "probability": "Medium",
                "mitigation": "Implement efficient irrigation methods. Use mulching to conserve moisture."
            })
        
        # Crop-specific risks
        if crop == "rice":
            risks.append({
                "type": "Pest",
                "risk": "Brown plant hopper and stem borer",
                "severity": "High",
                "probability": "High",
                "mitigation": "Use resistant varieties. Avoid excessive nitrogen. Monitor regularly."
            })
        elif crop == "cotton":
            risks.append({
                "type": "Pest",
                "risk": "Bollworm complex attack",
                "severity": "Critical",
                "probability": "Very High",
                "mitigation": "Use Bt cotton. Install pheromone traps. Regular scouting essential."
            })
        elif crop == "wheat":
            risks.append({
                "type": "Disease",
                "risk": "Yellow rust in humid conditions",
                "severity": "High",
                "probability": "Medium",
                "mitigation": "Use resistant varieties. Apply fungicides preventively if conditions favorable."
            })
        
        # Regional risks
        regional_risks = {
            "North": {
                "type": "Weather",
                "risk": "Terminal heat stress in late Rabi season",
                "severity": "Medium",
                "probability": "Medium",
                "mitigation": "Timely sowing. Use early-maturing varieties."
            },
            "South": {
                "type": "Weather",
                "risk": "Moisture stress in summer",
                "severity": "High",
                "probability": "High",
                "mitigation": "Drip irrigation. Mulching. Drought-tolerant varieties."
            },
            "East": {
                "type": "Weather",
                "risk": "Cyclone and extreme rainfall",
                "severity": "High",
                "probability": "Medium",
                "mitigation": "Crop insurance. Drainage systems. Disaster preparedness."
            },
            "West": {
                "type": "Water",
                "risk": "Prolonged dry spells",
                "severity": "High",
                "probability": "High",
                "mitigation": "Rainwater harvesting. Efficient irrigation. Crop selection."
            }
        }
        
        if region in regional_risks:
            risks.append(regional_risks[region])
        
        return risks
    
    def get_recommendations(self, crop: str, season: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Get best practices recommendations for crop cultivation
        
        Returns:
            Dictionary with categorized recommendations
        """
        crop = crop.lower()
        
        recommendations = {
            "seed_selection": [
                f"Use certified seeds of high-yielding {crop} varieties",
                "Choose disease-resistant varieties for your region",
                "Treat seeds with recommended fungicides before sowing"
            ],
            "soil_preparation": [
                "Conduct soil testing to determine nutrient status",
                "Apply organic manure (FYM) @ 10-15 tons/ha",
                "Ensure proper land leveling for uniform irrigation"
            ],
            "nutrient_management": [
                "Apply fertilizers based on soil test recommendations",
                "Follow split application of nitrogen for better efficiency",
                "Use micronutrients if deficiency symptoms observed"
            ],
            "irrigation": [
                "Provide irrigation at critical growth stages",
                "Implement efficient irrigation methods (drip/sprinkler)",
                "Avoid water stress during flowering and grain filling"
            ],
            "pest_management": [
                "Regular monitoring for pests and diseases",
                "Implement Integrated Pest Management (IPM) practices",
                "Use biopesticides and natural enemies when possible",
                "Apply chemical pesticides only when threshold is crossed"
            ],
            "harvest_management": [
                "Harvest at proper maturity for best quality and market price",
                "Ensure proper drying before storage",
                "Use appropriate post-harvest handling to minimize losses"
            ]
        }
        
        # Add season-specific recommendations
        if season:
            season = season.lower()
            if season == "kharif":
                recommendations["season_specific"] = [
                    "Ensure good drainage to prevent waterlogging",
                    "Monitor weather forecasts regularly during monsoon",
                    "Be prepared for pest pressure due to humidity"
                ]
            elif season == "rabi":
                recommendations["season_specific"] = [
                    "Plan irrigation schedule carefully",
                    "Protect crops from frost if in northern regions",
                    "Take advantage of cooler temperatures for better quality"
                ]
        
        return recommendations
    
    def get_seasonal_calendar(self, crop: str) -> Dict[str, str]:
        """
        Get crop calendar with important activities and timelines
        """
        crop = crop.lower()
        
        calendars = {
            "rice": {
                "land_preparation": "15-20 days before sowing",
                "nursery_sowing": "June (Kharif) / November (Rabi)",
                "transplanting": "July (Kharif) / December (Rabi)",
                "first_weeding": "20-25 days after transplanting",
                "top_dressing": "30-35 days after transplanting",
                "flowering": "60-80 days after transplanting",
                "maturity": "110-130 days after transplanting",
                "harvest": "September-October (Kharif) / March-April (Rabi)"
            },
            "wheat": {
                "land_preparation": "October-November",
                "sowing": "Mid-November to early December",
                "first_irrigation": "21 days after sowing (CRI stage)",
                "second_irrigation": "Tillering stage (40-45 days)",
                "third_irrigation": "Jointing stage (60-65 days)",
                "fourth_irrigation": "Flowering stage (80-85 days)",
                "fifth_irrigation": "Milk stage (100-105 days)",
                "harvest": "March-April"
            }
        }
        
        return calendars.get(crop, {
            "note": f"Detailed calendar for {crop} not available. Consult local agriculture department."
        })
    
    def analyze_trend(self, yield_data: List[Dict]) -> Dict[str, any]:
        """
        Analyze yield trends from historical data
        Simple trend analysis without ML
        """
        if len(yield_data) < 2:
            return {
                "trend": "insufficient_data",
                "message": "Need at least 2 years of data for trend analysis"
            }
        
        # Sort by year
        yield_data = sorted(yield_data, key=lambda x: x.get('year', 0))
        
        yields = [d['yield_tons'] for d in yield_data if 'yield_tons' in d]
        
        if not yields:
            return {"trend": "no_data", "message": "No yield data available"}
        
        # Calculate simple trend
        avg_yield = sum(yields) / len(yields)
        first_half = yields[:len(yields)//2]
        second_half = yields[len(yields)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        change_percent = ((avg_second - avg_first) / avg_first) * 100
        
        if change_percent > 5:
            trend_direction = "increasing"
            interpretation = "Yields are showing positive growth trend"
        elif change_percent < -5:
            trend_direction = "decreasing"
            interpretation = "Yields are showing declining trend - investigation needed"
        else:
            trend_direction = "stable"
            interpretation = "Yields are relatively stable"
        
        return {
            "trend": trend_direction,
            "average_yield": round(avg_yield, 2),
            "change_percent": round(change_percent, 2),
            "interpretation": interpretation,
            "recommendation": self._get_trend_recommendation(trend_direction)
        }
    
    def _get_trend_recommendation(self, trend: str) -> str:
        """Get recommendation based on trend"""
        if trend == "increasing":
            return "Continue current good practices. Document successful methods for replication."
        elif trend == "decreasing":
            return "Analyze causes: soil degradation, pest resistance, or management issues. Conduct soil testing and review practices."
        else:
            return "Maintain current practices but explore opportunities for yield improvement through better varieties or technologies."


# Example usage and testing
if __name__ == "__main__":
    ai = AIService()
    
    # Test advisory
    advisory = ai.get_crop_advisory("Rice", "Kharif", "North")
    print("Advisory for Rice in Kharif season:")
    print(advisory)
    
    # Test risk assessment
    risks = ai.assess_risks("Cotton", "South", "Kharif")
    print("\nRisk assessment:")
    for risk in risks:
        print(risk)
    
    # Test recommendations
    recommendations = ai.get_recommendations("Wheat", "Rabi")
    print("\nRecommendations:")
    print(recommendations)