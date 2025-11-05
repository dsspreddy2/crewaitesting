"""
Enhanced CrewAI Restaurant Recommender with Ollama (Neural Chat 7B)
Includes: Weather, Peak Time, Address, Dietary Restrictions, Ambiance
"""

from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_community.tools import Tool
import json
from datetime import datetime

# Initialize Ollama LLM (Neural Chat 7B)
# Make sure Ollama is running: ollama serve
llm = Ollama(
    model="neural-chat",
    base_url="http://localhost:11434",
    temperature=0.7,
    top_p=0.9,
    num_ctx=2048  # Context window size
)


# ============================================================================
# TOOLS DEFINITION
# ============================================================================

def restaurant_search_tool(query: str) -> str:
    """
    Simulated restaurant search tool with enhanced properties.
    In production, this would connect to Google Maps API, Yelp, or similar.
    
    Returns restaurants with: name, cuisine, rating, price, address, 
    weather suitability, peak hours, dietary options, ambiance
    """
    
    # Simulated restaurant database with enhanced properties
    restaurants_db = {
        "San Francisco": [
            {
                "name": "Greens Restaurant",
                "cuisine": "Vegetarian/Vegan",
                "rating": 4.8,
                "price_range": "$$$",
                "address": "Building A, Fort Mason, San Francisco, CA 94123",
                "weather_suitable": ["sunny", "clear", "partly_cloudy"],
                "peak_hours": "12:00-13:30, 18:00-20:00",
                "dietary_options": ["vegan", "vegetarian", "gluten-free"],
                "ambiance": "upscale, romantic, with bay view",
                "special_features": ["outdoor seating", "bay view", "wine selection"]
            },
            {
                "name": "State Bird Provisions",
                "cuisine": "American/Asian Fusion",
                "rating": 4.7,
                "price_range": "$$",
                "address": "1529 Fillmore St, San Francisco, CA 94115",
                "weather_suitable": ["any"],
                "peak_hours": "11:30-13:00, 17:30-19:30",
                "dietary_options": ["vegetarian", "pescatarian"],
                "ambiance": "casual, trendy, intimate",
                "special_features": ["dim sum style", "creative plating", "intimate setting"]
            },
            {
                "name": "Gary Danko",
                "cuisine": "French/Contemporary",
                "rating": 4.9,
                "price_range": "$$$$",
                "address": "800 North Point St, San Francisco, CA 94109",
                "weather_suitable": ["any"],
                "peak_hours": "17:30-19:00, 20:00-21:30",
                "dietary_options": ["vegetarian", "gluten-free"],
                "ambiance": "fine dining, elegant, upscale",
                "special_features": ["michelin star", "tasting menu", "sommelier service"]
            }
        ],
        "Berlin": [
            {
                "name": "Nobelhart & Schmutzig",
                "cuisine": "German/Contemporary",
                "rating": 4.8,
                "price_range": "$$$",
                "address": "Friedrichstr. 218, 10969 Berlin, Germany",
                "weather_suitable": ["any"],
                "peak_hours": "18:00-19:30, 20:30-22:00",
                "dietary_options": ["vegetarian"],
                "ambiance": "fine dining, modern, minimalist",
                "special_features": ["michelin star", "local ingredients", "tasting menu"]
            },
            {
                "name": "Mustafa's Gemüse Kebap",
                "cuisine": "Turkish/Street Food",
                "rating": 4.6,
                "price_range": "$",
                "address": "Mehringdamm 32, 10961 Berlin, Germany",
                "weather_suitable": ["sunny", "clear"],
                "peak_hours": "12:00-14:00, 18:00-22:00",
                "dietary_options": ["vegetarian", "vegan"],
                "ambiance": "casual, street food, lively",
                "special_features": ["famous kebab", "quick service", "budget-friendly"]
            },
            {
                "name": "Zur Letzten Instanz",
                "cuisine": "German/Traditional",
                "rating": 4.5,
                "price_range": "$$",
                "address": "Waisenstr. 14-16, 10179 Berlin, Germany",
                "weather_suitable": ["any"],
                "peak_hours": "12:00-14:00, 18:00-21:00",
                "dietary_options": ["vegetarian"],
                "ambiance": "traditional, cozy, historic",
                "special_features": ["oldest restaurant in Berlin", "traditional decor", "beer selection"]
            }
        ],
        "Tokyo": [
            {
                "name": "Sukiyabashi Jiro",
                "cuisine": "Sushi/Japanese",
                "rating": 4.9,
                "price_range": "$$$$",
                "address": "4 Chome-2-15 Ginza, Chuo City, Tokyo 104-0061, Japan",
                "weather_suitable": ["any"],
                "peak_hours": "11:30-14:00, 16:30-20:30",
                "dietary_options": ["pescatarian"],
                "ambiance": "fine dining, minimalist, intimate",
                "special_features": ["3 michelin stars", "omakase only", "counter seating"]
            },
            {
                "name": "Ichiran Ramen",
                "cuisine": "Ramen/Japanese",
                "rating": 4.4,
                "price_range": "$",
                "address": "Multiple locations in Tokyo",
                "weather_suitable": ["any"],
                "peak_hours": "11:30-14:00, 17:00-22:00",
                "dietary_options": ["vegetarian option available"],
                "ambiance": "casual, lively, counter seating",
                "special_features": ["famous ramen chain", "quick service", "individual booths"]
            }
        ]
    }
    
    # Parse query to extract location
    location = None
    for city in restaurants_db.keys():
        if city.lower() in query.lower():
            location = city
            break
    
    if not location:
        location = "San Francisco"  # Default
    
    # Get restaurants for the location
    restaurants = restaurants_db.get(location, [])
    
    # Format output
    output = f"Found {len(restaurants)} restaurants in {location}:\n\n"
    for i, rest in enumerate(restaurants, 1):
        output += f"{i}. {rest['name']}\n"
        output += f"   Cuisine: {rest['cuisine']}\n"
        output += f"   Rating: {rest['rating']}/5.0\n"
        output += f"   Price: {rest['price_range']}\n"
        output += f"   Address: {rest['address']}\n"
        output += f"   Weather Suitable: {', '.join(rest['weather_suitable'])}\n"
        output += f"   Peak Hours: {rest['peak_hours']}\n"
        output += f"   Dietary Options: {', '.join(rest['dietary_options'])}\n"
        output += f"   Ambiance: {rest['ambiance']}\n"
        output += f"   Special Features: {', '.join(rest['special_features'])}\n\n"
    
    return output


def weather_tool(location: str) -> str:
    """
    Simulated weather tool.
    In production, this would call OpenWeatherMap API or similar.
    """
    
    weather_db = {
        "San Francisco": {
            "current": "Partly Cloudy",
            "temperature": "65°F",
            "humidity": "65%",
            "wind": "10 mph",
            "recommendation": "Perfect for outdoor dining with a light jacket"
        },
        "Berlin": {
            "current": "Sunny",
            "temperature": "72°F",
            "humidity": "55%",
            "wind": "8 mph",
            "recommendation": "Excellent weather for outdoor seating"
        },
        "Tokyo": {
            "current": "Clear",
            "temperature": "68°F",
            "humidity": "60%",
            "wind": "5 mph",
            "recommendation": "Beautiful weather, perfect for any dining experience"
        }
    }
    
    weather = weather_db.get(location, weather_db["San Francisco"])
    
    output = f"Weather in {location}:\n"
    output += f"Current: {weather['current']}\n"
    output += f"Temperature: {weather['temperature']}\n"
    output += f"Humidity: {weather['humidity']}\n"
    output += f"Wind: {weather['wind']}\n"
    output += f"Recommendation: {weather['recommendation']}\n"
    
    return output


def peak_time_tool(restaurant_name: str) -> str:
    """
    Provides information about peak dining hours and recommendations.
    """
    
    peak_info = {
        "Greens Restaurant": {
            "peak_hours": "12:00-13:30 (lunch), 18:00-20:00 (dinner)",
            "best_time": "14:00-17:00 or after 20:30",
            "wait_time_peak": "30-45 minutes",
            "wait_time_off_peak": "5-10 minutes"
        },
        "State Bird Provisions": {
            "peak_hours": "11:30-13:00 (lunch), 17:30-19:30 (dinner)",
            "best_time": "13:30-17:00 or after 20:00",
            "wait_time_peak": "45-60 minutes",
            "wait_time_off_peak": "10-15 minutes"
        },
        "Gary Danko": {
            "peak_hours": "17:30-19:00, 20:00-21:30",
            "best_time": "Reservation required (no walk-ins)",
            "wait_time_peak": "N/A - Reservation only",
            "wait_time_off_peak": "N/A - Reservation only"
        }
    }
    
    info = peak_info.get(restaurant_name, {
        "peak_hours": "12:00-14:00, 18:00-20:00",
        "best_time": "Off-peak hours recommended",
        "wait_time_peak": "20-30 minutes",
        "wait_time_off_peak": "5-10 minutes"
    })
    
    output = f"Peak Time Information for {restaurant_name}:\n"
    output += f"Peak Hours: {info['peak_hours']}\n"
    output += f"Best Time to Visit: {info['best_time']}\n"
    output += f"Wait Time (Peak): {info['wait_time_peak']}\n"
    output += f"Wait Time (Off-Peak): {info['wait_time_off_peak']}\n"
    
    return output


def dietary_restrictions_tool(dietary_preference: str) -> str:
    """
    Filters restaurants based on dietary restrictions.
    """
    
    dietary_db = {
        "vegan": ["Greens Restaurant", "State Bird Provisions", "Mustafa's Gemüse Kebap"],
        "vegetarian": ["Greens Restaurant", "State Bird Provisions", "Nobelhart & Schmutzig", "Mustafa's Gemüse Kebap", "Zur Letzten Instanz"],
        "gluten-free": ["Greens Restaurant", "Gary Danko", "Sukiyabashi Jiro"],
        "pescatarian": ["State Bird Provisions", "Sukiyabashi Jiro"],
        "halal": ["Mustafa's Gemüse Kebap"],
        "kosher": []
    }
    
    restaurants = dietary_db.get(dietary_preference.lower(), [])
    
    if restaurants:
        output = f"Restaurants suitable for {dietary_preference} diet:\n"
        for rest in restaurants:
            output += f"• {rest}\n"
    else:
        output = f"No restaurants found with {dietary_preference} options in our database."
    
    return output


def ambiance_tool(ambiance_type: str) -> str:
    """
    Recommends restaurants based on desired ambiance.
    """
    
    ambiance_db = {
        "romantic": ["Greens Restaurant", "Gary Danko"],
        "casual": ["State Bird Provisions", "Mustafa's Gemüse Kebap", "Ichiran Ramen"],
        "fine dining": ["Gary Danko", "Nobelhart & Schmutzig", "Sukiyabashi Jiro"],
        "business": ["Gary Danko", "Nobelhart & Schmutzig"],
        "family-friendly": ["State Bird Provisions", "Ichiran Ramen"],
        "trendy": ["State Bird Provisions"],
        "traditional": ["Zur Letzten Instanz"],
        "upscale": ["Greens Restaurant", "Gary Danko"]
    }
    
    restaurants = ambiance_db.get(ambiance_type.lower(), [])
    
    if restaurants:
        output = f"Restaurants with {ambiance_type} ambiance:\n"
        for rest in restaurants:
            output += f"• {rest}\n"
    else:
        output = f"No restaurants found with {ambiance_type} ambiance in our database."
    
    return output


# ============================================================================
# TOOL WRAPPERS FOR CREWAI
# ============================================================================

restaurant_search = Tool(
    name="Restaurant Search",
    func=restaurant_search_tool,
    description="Search for restaurants with detailed information including address, weather suitability, peak hours, dietary options, and ambiance"
)

weather_info = Tool(
    name="Weather Information",
    func=weather_tool,
    description="Get current weather conditions and recommendations for a specific location"
)

peak_time_info = Tool(
    name="Peak Time Information",
    func=peak_time_tool,
    description="Get peak dining hours and wait times for a specific restaurant"
)

dietary_filter = Tool(
    name="Dietary Restrictions Filter",
    func=dietary_restrictions_tool,
    description="Filter restaurants based on dietary preferences (vegan, vegetarian, gluten-free, etc.)"
)

ambiance_filter = Tool(
    name="Ambiance Filter",
    func=ambiance_tool,
    description="Find restaurants with specific ambiance (romantic, casual, fine dining, etc.)"
)

tools = [restaurant_search, weather_info, peak_time_info, dietary_filter, ambiance_filter]


# ============================================================================
# AGENTS DEFINITION
# ============================================================================

# Agent 1: Restaurant Researcher
researcher = Agent(
    role="Restaurant Researcher",
    goal="Find the best restaurant options that match user preferences, including location, cuisine, ratings, and special features",
    backstory="""You are an expert restaurant researcher with deep knowledge of dining establishments worldwide. 
    You excel at finding restaurants that match specific criteria and gathering comprehensive information about them. 
    You use the Restaurant Search tool to find options and consider factors like address, peak hours, and special features.""",
    tools=[restaurant_search],
    llm=llm,
    verbose=True
)

# Agent 2: Enhanced Analyst (considers weather, peak time, dietary, ambiance)
analyst = Agent(
    role="Dining Experience Analyst",
    goal="Analyze restaurant options considering weather, peak hours, dietary restrictions, and ambiance to identify the best choice",
    backstory="""You are an expert dining consultant who considers multiple factors when recommending restaurants. 
    You analyze weather conditions, peak dining hours, dietary requirements, and desired ambiance. 
    You use multiple tools to gather comprehensive information and make the best recommendation based on all factors.""",
    tools=[weather_info, peak_time_info, dietary_filter, ambiance_filter],
    llm=llm,
    verbose=True
)

# Agent 3: Recommendation Generator
generator = Agent(
    role="Personalized Recommendation Generator",
    goal="Create compelling, detailed restaurant recommendations that address all user preferences and considerations",
    backstory="""You are a professional concierge with exceptional communication skills. 
    You craft personalized, persuasive recommendations that explain why a restaurant is perfect for the user. 
    You consider weather, timing, dietary needs, and ambiance to create a compelling narrative around your recommendation.""",
    tools=[],
    llm=llm,
    verbose=True
)


# ============================================================================
# TASKS DEFINITION
# ============================================================================

# Task 1: Research
research_task = Task(
    description="""Search for restaurants matching these preferences: {user_preferences}
    
    Use the Restaurant Search tool to find 3-5 options. Include:
    - Restaurant name and cuisine type
    - Rating and price range
    - Full address
    - Peak dining hours
    - Dietary options available
    - Ambiance and special features
    
    Provide a structured list of options with all details.""",
    expected_output="A detailed list of 3-5 restaurant options with complete information",
    agent=researcher
)

# Task 2: Analysis
analysis_task = Task(
    description="""Analyze the restaurants found by the Researcher considering:
    1. Current weather conditions for the location
    2. Peak dining hours and wait times
    3. Dietary restrictions: {dietary_restrictions}
    4. Desired ambiance: {ambiance_preference}
    
    Use the Weather Information, Peak Time Information, Dietary Restrictions Filter, and Ambiance Filter tools.
    
    Evaluate each restaurant against these criteria and identify the SINGLE BEST recommendation.
    Explain your reasoning for each factor considered.""",
    expected_output="A detailed analysis with a clear recommendation and reasoning for why it's the best choice",
    agent=analyst
)

# Task 3: Generation
generation_task = Task(
    description="""Based on the Analyst's recommendation, create a personalized restaurant recommendation that includes:
    
    1. Restaurant name and why it's perfect for this user
    2. Address and how to get there
    3. Why it matches their dietary preferences: {dietary_restrictions}
    4. Why the ambiance suits them: {ambiance_preference}
    5. Best time to visit considering peak hours and current weather
    6. What to expect (cuisine, price, special features)
    7. A compelling reason to visit this restaurant
    
    Write in a friendly, persuasive tone that makes the user excited about this recommendation.""",
    expected_output="A personalized, compelling restaurant recommendation with all relevant details",
    agent=generator
)


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def create_crew():
    """Create and return the CrewAI crew"""
    crew = Crew(
        agents=[researcher, analyst, generator],
        tasks=[research_task, analysis_task, generation_task],
        verbose=True
    )
    return crew


def get_recommendation(user_preferences: str, dietary_restrictions: str = "no restrictions", 
                       ambiance_preference: str = "casual") -> str:
    """
    Main function to get a restaurant recommendation
    
    Args:
        user_preferences: User's dining preferences (location, cuisine, etc.)
        dietary_restrictions: Dietary needs (vegan, vegetarian, gluten-free, etc.)
        ambiance_preference: Desired ambiance (romantic, casual, fine dining, etc.)
    
    Returns:
        Personalized restaurant recommendation
    """
    
    crew = create_crew()
    
    # Prepare inputs for tasks
    inputs = {
        "user_preferences": user_preferences,
        "dietary_restrictions": dietary_restrictions,
        "ambiance_preference": ambiance_preference
    }
    
    # Execute the crew
    result = crew.kickoff(inputs=inputs)
    
    return result


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🚀 Testing Enhanced Ollama-based CrewAI Restaurant Recommender\n")
    print("=" * 80)
    
    # Test query
    user_prefs = "I'm looking for an affordable restaurant in San Francisco with a rating above 4.0"
    dietary = "vegan-friendly"
    ambiance = "romantic with a view"
    
    print(f"User Preferences: {user_prefs}")
    print(f"Dietary Restrictions: {dietary}")
    print(f"Ambiance Preference: {ambiance}")
    print("=" * 80)
    print()
    
    recommendation = get_recommendation(user_prefs, dietary, ambiance)
    
    print("\n" + "=" * 80)
    print("FINAL RECOMMENDATION:")
    print("=" * 80)
    print(recommendation)
