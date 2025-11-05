import streamlit as st
from crew import run_crew
import os

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="CrewAI Restaurant Recommender",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header and Description ---
st.title("🍽️ CrewAI Restaurant Recommender")
st.markdown("""
Welcome to the **CrewAI Restaurant Recommender** demo! 
This application uses a multi-agent system built with **CrewAI** to provide personalized restaurant recommendations. 
The agents collaborate to research, analyze, and generate a final, tailored suggestion based on your preferences.

This demo is designed to be run on an AWS EC2 instance and uses the pre-configured **OpenAI API** (via `gpt-4.1-mini`) for a cost-effective demonstration.
""")

# --- Sidebar for Instructions ---
with st.sidebar:
    st.header("How the Crew Works")
    st.markdown("""
    1. **Restaurant Researcher:** Gathers initial data on 3-5 top-rated restaurants based on your input.
    2. **Cuisine Analyst:** Analyzes the list, focusing on ratings, trends, and unique features.
    3. **Recommendation Generator:** Synthesizes the analysis into a final, personalized recommendation.
    
    The process is sequential, and the agents delegate tasks to each other. The detailed collaboration log will be visible in the terminal where the Streamlit app is running.
    """)
    
    st.info("Example Preference: 'A romantic, high-end French restaurant in New York City with a 5-star rating.'")

# --- Main Application Logic ---

# Input field for user preferences
user_preference = st.text_area(
    "Tell us your dining preferences (Cuisine, Location, Price Range, Occasion, etc.):",
    value="Affordable Italian restaurant in downtown Chicago with a rating above 4.0",
    height=100
)

# Button to trigger the recommendation
if st.button("Get Recommendation", type="primary"):
    if not user_preference:
        st.error("Please enter your dining preferences to get a recommendation.")
    else:
        # Display a spinner while the crew is running
        with st.spinner("Agents are collaborating to find your perfect restaurant... (Check terminal for verbose log)"):
            try:
                # Run the CrewAI process
                final_recommendation = run_crew(user_preference)
                
                # Display the result
                st.success("Recommendation Complete!")
                st.markdown("---")
                st.subheader("Your Personalized Restaurant Recommendation:")
                st.markdown(final_recommendation)
                st.markdown("---")

            except Exception as e:
                st.error(f"An error occurred during the CrewAI process. Please check the terminal for details.")
                st.exception(e)
