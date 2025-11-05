"""
Enhanced Streamlit Application for CrewAI Restaurant Recommender with Ollama
Features: Weather, Peak Time, Address, Dietary Restrictions, Ambiance
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import crew_ollama
sys.path.insert(0, str(Path(__file__).parent))

from crew_ollama import get_recommendation

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="CrewAI Restaurant Recommender (Ollama)",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5em;
    }
    .sub-header {
        font-size: 1.2em;
        color: #555;
        margin-bottom: 1em;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        border-left: 4px solid #28a745;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        border-left: 4px solid #17a2b8;
    }
    .recommendation-box {
        background-color: #fff3cd;
        padding: 1.5em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        border-left: 4px solid #ffc107;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("### 🔧 System Information")
    st.info("""
    **Ollama Version - Enhanced Features**
    
    ✅ No API tokens required
    ✅ Local Neural Chat 7B model
    ✅ Weather integration
    ✅ Peak time analysis
    ✅ Dietary restrictions
    ✅ Ambiance preferences
    ✅ Address details
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 How the System Works")
    with st.expander("Agent 1: Researcher", expanded=False):
        st.write("""
        **Role:** Restaurant Researcher
        
        Searches for restaurants matching your preferences and gathers:
        - Restaurant name and cuisine
        - Ratings and price range
        - Full address and location
        - Peak dining hours
        - Dietary options
        - Special features
        """)
    
    with st.expander("Agent 2: Analyst", expanded=False):
        st.write("""
        **Role:** Dining Experience Analyst
        
        Analyzes restaurants considering:
        - Current weather conditions
        - Peak hours and wait times
        - Your dietary restrictions
        - Desired ambiance
        - Overall suitability
        """)
    
    with st.expander("Agent 3: Generator", expanded=False):
        st.write("""
        **Role:** Recommendation Generator
        
        Creates personalized recommendations including:
        - Why this restaurant is perfect for you
        - How to get there
        - Best time to visit
        - What to expect
        - Compelling reasons to visit
        """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    st.write("**Model:** Neural Chat 7B (Ollama)")
    st.write("**Instance Type:** AWS g5.xlarge")
    st.write("**GPU:** NVIDIA A10G (24GB VRAM)")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown('<div class="main-header">🍽️ CrewAI Restaurant Recommender</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enhanced with Weather, Peak Time, Address & More</div>', 
            unsafe_allow_html=True)

st.markdown("""
<div class="feature-box">
Welcome to the enhanced Ollama-powered restaurant recommendation system! This application uses a team of specialized AI agents to provide personalized restaurant recommendations considering multiple factors like weather, peak hours, dietary restrictions, and ambiance preferences.

**Key Features:**
- 🌤️ Weather-aware recommendations
- ⏰ Peak time analysis and wait time estimates
- 🏠 Detailed address information
- 🥗 Dietary restriction filtering
- 🎭 Ambiance preference matching
- 🤖 Multi-agent AI collaboration
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INPUT FORM
# ============================================================================

st.markdown("### 🔍 Tell Us Your Preferences")

col1, col2 = st.columns(2)

with col1:
    # Main preferences
    st.markdown("**Basic Preferences**")
    
    user_preferences = st.text_area(
        "What are you looking for in a restaurant?",
        placeholder="e.g., 'An affordable restaurant in San Francisco with a rating above 4.0 close to the waterfront'",
        height=100,
        key="preferences"
    )
    
    location = st.selectbox(
        "Preferred Location",
        ["San Francisco", "Berlin", "Tokyo", "Other"],
        key="location"
    )
    
    if location == "Other":
        location = st.text_input("Enter your preferred location:")

with col2:
    # Enhanced preferences
    st.markdown("**Enhanced Preferences**")
    
    dietary_restrictions = st.multiselect(
        "Dietary Restrictions",
        ["None", "Vegan", "Vegetarian", "Gluten-Free", "Pescatarian", "Halal", "Kosher"],
        default=["None"],
        key="dietary"
    )
    
    # Convert to string
    if "None" in dietary_restrictions or len(dietary_restrictions) == 0:
        dietary_str = "No restrictions"
    else:
        dietary_str = ", ".join(dietary_restrictions)
    
    ambiance_preference = st.multiselect(
        "Desired Ambiance",
        ["Casual", "Romantic", "Fine Dining", "Business", "Family-Friendly", "Trendy", "Traditional", "Upscale"],
        default=["Casual"],
        key="ambiance"
    )
    
    # Convert to string
    ambiance_str = ", ".join(ambiance_preference) if ambiance_preference else "Casual"

# Additional preferences
st.markdown("**Additional Considerations**")

col3, col4, col5 = st.columns(3)

with col3:
    cuisine_preference = st.text_input(
        "Preferred Cuisine (optional)",
        placeholder="e.g., Italian, Asian, Mediterranean",
        key="cuisine"
    )

with col4:
    price_range = st.selectbox(
        "Price Range",
        ["Any", "$", "$$", "$$$", "$$$$"],
        key="price"
    )

with col5:
    party_size = st.number_input(
        "Party Size",
        min_value=1,
        max_value=20,
        value=2,
        key="party_size"
    )

# ============================================================================
# SUBMISSION AND PROCESSING
# ============================================================================

st.markdown("---")

col_button1, col_button2, col_button3 = st.columns([1, 1, 1])

with col_button1:
    submit_button = st.button(
        "🚀 Get Recommendation",
        use_container_width=True,
        type="primary"
    )

with col_button2:
    clear_button = st.button(
        "🔄 Clear Form",
        use_container_width=True
    )

with col_button3:
    example_button = st.button(
        "📋 Load Example",
        use_container_width=True
    )

# Handle example button
if example_button:
    st.session_state.preferences = "A vegan-friendly restaurant in San Francisco with a view, suitable for a business dinner"
    st.session_state.location = "San Francisco"
    st.session_state.dietary = ["Vegan"]
    st.session_state.ambiance = ["Business", "Romantic"]
    st.session_state.cuisine = "Contemporary"
    st.session_state.price = "$$$"
    st.session_state.party_size = 2
    st.rerun()

# Handle clear button
if clear_button:
    st.session_state.preferences = ""
    st.session_state.location = "San Francisco"
    st.session_state.dietary = ["None"]
    st.session_state.ambiance = ["Casual"]
    st.session_state.cuisine = ""
    st.session_state.price = "Any"
    st.session_state.party_size = 2
    st.rerun()

# ============================================================================
# RECOMMENDATION PROCESSING
# ============================================================================

if submit_button:
    if not user_preferences.strip():
        st.error("❌ Please enter your dining preferences!")
    else:
        # Build full preference string
        full_preferences = f"{user_preferences}"
        if cuisine_preference:
            full_preferences += f", Cuisine: {cuisine_preference}"
        if price_range != "Any":
            full_preferences += f", Price: {price_range}"
        full_preferences += f", Party size: {party_size}"
        full_preferences += f", Location: {location}"
        
        # Show processing status
        with st.spinner("🤖 Agents are collaborating to find your perfect restaurant..."):
            st.markdown("""
            <div class="info-box">
            <strong>Processing:</strong>
            <br>🔍 Researcher is searching for options...
            <br>📊 Analyst is evaluating preferences...
            <br>✍️ Generator is crafting your recommendation...
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Get recommendation from crew
                recommendation = get_recommendation(
                    user_preferences=full_preferences,
                    dietary_restrictions=dietary_str,
                    ambiance_preference=ambiance_str
                )
                
                # Display recommendation
                st.markdown("""
                <div class="success-box">
                <strong>✅ Recommendation Complete!</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="recommendation-box">
                """, unsafe_allow_html=True)
                
                st.markdown("### 🏆 Your Personalized Restaurant Recommendation")
                st.markdown(recommendation)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display summary
                st.markdown("---")
                st.markdown("### 📋 Recommendation Summary")
                
                col_summary1, col_summary2 = st.columns(2)
                
                with col_summary1:
                    st.markdown(f"""
                    **Your Preferences:**
                    - Location: {location}
                    - Dietary: {dietary_str}
                    - Ambiance: {ambiance_str}
                    - Party Size: {party_size}
                    """)
                
                with col_summary2:
                    st.markdown(f"""
                    **Restaurant Details:**
                    - Cuisine: {cuisine_preference if cuisine_preference else 'Any'}
                    - Price Range: {price_range}
                    - Weather: Considered
                    - Peak Hours: Analyzed
                    """)
                
            except Exception as e:
                st.error(f"❌ Error generating recommendation: {str(e)}")
                st.info("Make sure Ollama is running: `ollama serve`")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("""
    <div style="text-align: center;">
    <small>
    🤖 Powered by CrewAI<br>
    🦙 Neural Chat 7B (Ollama)<br>
    ☁️ AWS g5.xlarge
    </small>
    </div>
    """, unsafe_allow_html=True)

with col_footer2:
    st.markdown("""
    <div style="text-align: center;">
    <small>
    ✅ No API Tokens Required<br>
    💰 Zero Per-Token Costs<br>
    🔒 100% Local Processing
    </small>
    </div>
    """, unsafe_allow_html=True)

with col_footer3:
    st.markdown("""
    <div style="text-align: center;">
    <small>
    📊 Multi-Agent System<br>
    🌤️ Weather-Aware<br>
    ⏰ Peak Time Analysis
    </small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 2em; padding: 1em; background-color: #f0f2f6; border-radius: 0.5em;">
<small>
<strong>System Status:</strong> ✅ Running on Ollama (Neural Chat 7B)<br>
<strong>Instance:</strong> AWS g5.xlarge with NVIDIA A10G GPU<br>
<strong>Version:</strong> Enhanced with Weather, Peak Time, Address & Ambiance
</small>
</div>
""", unsafe_allow_html=True)
