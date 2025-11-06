from typing import List

import requests
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai.tools import tool

# Import the real tool
from crewai_tools import SerperDevTool

# Initialize the real tool
restaurant_search_tool = SerperDevTool()


@tool("Dining Weather Lookup")
def fetch_weather_report(location: str) -> str:
    """Look up the current weather for the provided dining location and return a concise summary."""

    cleaned_location = location.strip()
    if not cleaned_location:
        return "No location provided for the weather lookup."

    try:
        geocode_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": cleaned_location, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        results = geocode_data.get("results") or []
        if not results:
            return f"No coordinates found for '{cleaned_location}'. Try a larger city or include the state/country."

        location_match = results[0]
        latitude = location_match.get("latitude")
        longitude = location_match.get("longitude")
        resolved_name = location_match.get("name")
        country = location_match.get("country")

        if latitude is None or longitude is None:
            return f"Could not determine coordinates for '{cleaned_location}'."

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
                "hourly": "precipitation_probability,weathercode",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current_weather = weather_data.get("current_weather") or {}
        temperature = current_weather.get("temperature")
        windspeed = current_weather.get("windspeed")
        weather_code = current_weather.get("weathercode")
        weather_time = current_weather.get("time")

        if temperature is None:
            return "Weather data is temporarily unavailable. Please try again later."

        weather_description = _WEATHER_CODES.get(weather_code, "current conditions")
        location_header = f"{resolved_name}, {country}" if country else resolved_name or cleaned_location

        hourly = weather_data.get("hourly") or {}
        precipitation_probabilities: List[float] = hourly.get("precipitation_probability") or []
        precipitation_summary = None
        if precipitation_probabilities:
            next_hours_prob = precipitation_probabilities[:6]
            avg_precip = sum(next_hours_prob) / len(next_hours_prob)
            precipitation_summary = f"Average precipitation chance next few hours: {avg_precip:.0f}%"

        summary_lines = [
            f"Weather for {location_header} at {weather_time}:",
            f"- Temperature: {temperature}°C",
            f"- Windspeed: {windspeed} km/h",
            f"- Conditions: {weather_description}",
        ]
        if precipitation_summary:
            summary_lines.append(f"- {precipitation_summary}")

        summary_lines.append(
            "Consider whether outdoor seating is comfortable and mention any contingency plans in your recommendation."
        )

        return "\n".join(summary_lines)

    except requests.RequestException as exc:
        return f"Weather service error: {exc}. Please try again with a different location or later."


_WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}

# --- Agents ---
researcher = Agent(
    role='Restaurant Researcher',
    goal='Gather initial data on top-rated restaurants based on user-provided cuisine, location, and price range.',
    backstory="A meticulous food critic who excels at finding hidden gems and popular spots. You are the first step in the recommendation process.",
    verbose=True,
    allow_delegation=False,
    tools=[restaurant_search_tool],
    llm=llm
)

analyzer = Agent(
    role='Cuisine and Trend Analyst',
    goal='Analyze the list of restaurants provided by the researcher, focusing on ratings, unique menu items, and current dining trends.',
    backstory="An expert in culinary trends and data analysis. You can spot patterns and identify the best value and experience from a list of options.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

generator = Agent(
    role='Personalized Recommendation Generator',
    goal='Synthesize the analyzed data into a final, personalized, and persuasive recommendation for the user.',
    backstory="A professional concierge who crafts perfect dining experiences. Your final output must be clear, engaging, and directly address the user's initial request.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

weather_specialist = Agent(
    role="Weather and Ambience Advisor",
    goal="Provide accurate, up-to-date weather insights for the dining location so guests can plan their experience.",
    backstory="A hospitality professional who monitors forecasts to ensure diners are prepared for patio seating, travel, and attire.",
    verbose=True,
    allow_delegation=False,
    tools=[fetch_weather_report],
    llm=llm,
)

# --- Tasks ---
def create_tasks(user_preference: str, include_weather: bool):
    """Creates the tasks for the crew based on user input."""

    task_research = Task(
        description=f"Use the 'Restaurant Search Tool' to find a list of 3-5 top-rated restaurants that match the user's preference: '{user_preference}'. The output must be a detailed, realistic list of restaurants, including name, cuisine, rating (e.g., 4.5/5), price range (e.g., $$$), and a brief description.",
        agent=researcher,
        expected_output="A markdown-formatted list of 3-5 restaurants with all required details (name, cuisine, rating, price, description)."
    )

    weather_task = None
    if include_weather:
        weather_task = Task(
            description=(
                "Determine the dining location referenced by the user preference or inferred from the researched restaurants. "
                "Use the 'Dining Weather Lookup' tool to gather the current weather conditions. Provide a concise summary of "
                "temperature, precipitation expectations, and any comfort considerations relevant to dining (e.g., patio suitability)."
            ),
            agent=weather_specialist,
            context=[task_research],
            expected_output=(
                "A short weather briefing for the identified location including temperature, wind, precipitation chances, "
                "and guidance on how the conditions affect dining plans."
            ),
        )

    task_analyze = Task(
        description="Review the list of restaurants provided by the researcher. For each restaurant, analyze its key features, unique selling points, and why it would be a good fit for the user. Identify the single best recommendation.",
        agent=analyzer,
        context=[task_research] + ([weather_task] if weather_task else []),
        expected_output=(
            "A detailed analysis of the top 3-5 restaurants, referencing any relevant weather considerations when applicable, "
            "and concluding with a clear identification of the single best recommendation and the reasons why."
        ),
    )

    task_generate = Task(
        description="Based on the analysis, write a final, engaging, and personalized recommendation. The output should be a single, well-structured markdown response that presents the best restaurant and a brief mention of the runner-up options.",
        agent=generator,
        context=[task_analyze] + ([weather_task] if weather_task else []),
        expected_output=(
            "A final, personalized restaurant recommendation in a friendly, professional tone, formatted in markdown, and "
            "including actionable weather insights when they are available."
        ),
    )

    tasks = [task_research]
    if weather_task:
        tasks.append(weather_task)
    tasks.extend([task_analyze, task_generate])

    return tasks

# --- Crew Setup Function ---
def run_crew(user_preference: str, include_weather: bool = True) -> str:
    """Initializes and runs the CrewAI process."""

    tasks = create_tasks(user_preference, include_weather)

    agents = [researcher]
    if include_weather:
        agents.append(weather_specialist)
    agents.extend([analyzer, generator])

    restaurant_crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    
    print("Starting Restaurant Recommendation Crew...")
    result = restaurant_crew.kickoff()
    print("Crew finished.")
    
    return result

if __name__ == '__main__':
    example_preference = "Affordable Italian restaurant in downtown Chicago with a rating above 4.0"
    print(f"\n--- Running Crew for: {example_preference} ---\n")
    recommendation = run_crew(example_preference)
    print("\n\n--- FINAL RECOMMENDATION ---\n")
    print(recommendation)
