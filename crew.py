import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai.tools import tool

# --- Configuration ---
llm = ChatOpenAI(model="gpt-4.1-mini")

# --- Tools ---
@tool("Restaurant Search Tool")
def restaurant_search_tool(query: str) -> str:
    """Simulates a search for restaurants based on a query.
    The query should contain cuisine, location, and price range.
    """
    return f"Simulated search for: {query}. The agent should now use its knowledge to provide a detailed, realistic list of 3-5 top-rated restaurants matching this criteria, including their name, cuisine, rating, and a brief description."

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

# --- Tasks ---
def create_tasks(user_preference: str):
    """Creates the tasks for the crew based on user input."""
    
    task_research = Task(
        description=f"Use the 'Restaurant Search Tool' to find a list of 3-5 top-rated restaurants that match the user's preference: '{user_preference}'. The output must be a detailed, realistic list of restaurants, including name, cuisine, rating (e.g., 4.5/5), price range (e.g., $$$), and a brief description.",
        agent=researcher,
        expected_output="A markdown-formatted list of 3-5 restaurants with all required details (name, cuisine, rating, price, description)."
    )

    task_analyze = Task(
        description="Review the list of restaurants provided by the researcher. For each restaurant, analyze its key features, unique selling points, and why it would be a good fit for the user. Identify the single best recommendation.",
        agent=analyzer,
        context=[task_research],
        expected_output="A detailed analysis of the top 3-5 restaurants, concluding with a clear identification of the single best recommendation and the reasons why."
    )

    task_generate = Task(
        description="Based on the analysis, write a final, engaging, and personalized recommendation. The output should be a single, well-structured markdown response that presents the best restaurant and a brief mention of the runner-up options.",
        agent=generator,
        context=[task_analyze],
        expected_output="A final, personalized restaurant recommendation in a friendly, professional tone, formatted in markdown."
    )
    
    return [task_research, task_analyze, task_generate]

# --- Crew Setup Function ---
def run_crew(user_preference: str) -> str:
    """Initializes and runs the CrewAI process."""
    
    tasks = create_tasks(user_preference)
    
    restaurant_crew = Crew(
        agents=[researcher, analyzer, generator],
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
