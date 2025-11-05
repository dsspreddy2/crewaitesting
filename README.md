# CrewAI Restaurant Recommender

A sophisticated multi-agent AI system that provides personalized restaurant recommendations using CrewAI, Streamlit, and OpenAI's language models. This project demonstrates the power of collaborative AI agents working together to solve complex problems efficiently and cost-effectively.

## 🎯 Project Overview

The **CrewAI Restaurant Recommender** showcases how specialized AI agents can collaborate sequentially to deliver superior results compared to a single AI model. The system uses three distinct agents—Researcher, Analyst, and Generator—each with specific expertise, working together to research, analyze, and generate personalized restaurant recommendations.

### Key Features

- **Multi-Agent Architecture:** Three specialized agents collaborate sequentially, each focusing on a specific task
- **Transparent Process:** Real-time logging shows exactly how each agent works and why decisions are made
- **Cost-Efficient:** Uses `gpt-4.1-mini` model, costing less than $0.005 per recommendation
- **Production-Ready:** Deployed on AWS EC2 with security best practices
- **User-Friendly Interface:** Simple Streamlit UI for non-technical users
- **Fully Open Source:** Complete code, documentation, and deployment guides included

## 🏗️ Architecture

### The Three-Agent System

#### 1. **Restaurant Researcher Agent**
- **Role:** Data Collector
- **Responsibility:** Takes user preferences and searches for 3-5 top-rated restaurant options
- **Output:** Structured list with restaurant name, cuisine, rating, price range, and description
- **Tools:** Restaurant Search Tool (simulated for demo; can be connected to real APIs)

#### 2. **Cuisine Analyst Agent**
- **Role:** Critical Thinker
- **Responsibility:** Analyzes the restaurant list based on ratings, trends, and user preferences
- **Output:** Detailed analysis with final recommendation and reasoning
- **Decision:** Identifies the single best restaurant that matches user criteria

#### 3. **Recommendation Generator Agent**
- **Role:** Concierge
- **Responsibility:** Crafts the final, personalized recommendation with engaging copy
- **Output:** Professional, persuasive recommendation ready for the user
- **Focus:** Presentation, tone, and user engagement

### Workflow

```
User Input
    ↓
Researcher Agent (Find Options)
    ↓
Analyst Agent (Evaluate & Decide)
    ↓
Generator Agent (Write Final Recommendation)
    ↓
Personalized Recommendation Output
```

Each agent receives context from the previous agent, enabling true collaboration and refinement of the recommendation at each step.

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))
- **Git** (for cloning and version control)
- **AWS EC2 Instance** (optional, for production deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/dsspreddy2/crewaitesting.git
cd crewaitesting
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your OpenAI API Key

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 6. Test the Application

1. Enter your dining preferences in the text box (e.g., "A vegan-friendly restaurant in San Francisco with a view")
2. Click "Get Recommendation"
3. Watch the agents collaborate in real-time
4. View the personalized recommendation

## 📁 Project Structure

```
crewaitesting/
├── app.py                              # Streamlit user interface
├── crew.py                             # CrewAI agents and tasks definition
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore file (excludes .env, logs, etc.)
├── README.md                           # This file
├── AWS_EC2_Deployment_Guide.md         # AWS EC2 deployment instructions
├── SPEAKER_NOTES.md                    # Detailed speaker notes for presentations
├── PRESENTATION_SCRIPT.md              # Full word-for-word presentation script
└── demo_presentation/                  # Team presentation slides
    ├── slide_1_intro.html
    ├── slide_2_how_it_works.html
    └── slide_3_live_demo.html
```

### File Descriptions

| File | Purpose |
| :--- | :--- |
| `app.py` | Streamlit application that provides the user interface |
| `crew.py` | Defines the three agents, their tasks, and the CrewAI workflow |
| `requirements.txt` | Lists all Python dependencies (CrewAI, Streamlit, OpenAI, etc.) |
| `.gitignore` | Prevents sensitive files (.env, API keys, logs) from being committed |
| `AWS_EC2_Deployment_Guide.md` | Step-by-step guide for deploying on AWS EC2 |
| `SPEAKER_NOTES.md` | Detailed talking points and explanations for presenters |
| `PRESENTATION_SCRIPT.md` | Complete word-for-word script for the 3-slide presentation |

## 🔧 Configuration

### Environment Variables

The application uses the following environment variable:

- **`OPENAI_API_KEY`**: Your OpenAI API key (required)

Set this before running the application:

```bash
export OPENAI_API_KEY="sk-..."
```

### Model Configuration

The application uses the **`gpt-4.1-mini`** model by default. This is a small, fast, and cost-effective model suitable for this use case. You can modify the model in `crew.py` if needed:

```python
llm=ChatOpenAI(model="gpt-4.1-mini")
```

### Cost Estimation

- **Per Recommendation:** < $0.005 (less than half a cent)
- **100 Recommendations:** < $0.50
- **1,000 Recommendations:** < $5.00

## 📚 Technology Stack

| Technology | Purpose | Version |
| :--- | :--- | :--- |
| **CrewAI** | Multi-agent orchestration framework | Latest |
| **Streamlit** | Web UI framework | Latest |
| **OpenAI API** | Language model (gpt-4.1-mini) | Latest |
| **LangChain** | LLM integration | Latest |
| **Python** | Programming language | 3.8+ |

## 🎓 How It Works: Detailed Explanation

### Step 1: User Input
The user enters their dining preferences through the Streamlit interface:
```
"I'm looking for an affordable Deutsch restaurant in Stanberg with a rating above 4.0 which is close to Stanberg see"
```

### Step 2: Researcher Agent Activates
The Researcher uses the Restaurant Search Tool to find matching restaurants:
```
Tool: Restaurant Search Tool
Input: Affordable Deutsch restaurant in Stanberg, rating > 4.0
Output: [List of 3-5 restaurants with details]
```

### Step 3: Analyst Agent Reviews
The Analyst evaluates each restaurant and selects the best match:
```
Analysis: Comparing ratings, price, cuisine, location
Decision: "Zum Alten Wirt is the best match because..."
```

### Step 4: Generator Agent Writes
The Generator crafts the final recommendation:
```
Output: "Your Top Dining Choice Near Starnberger See: Zum Alten Wirt..."
```

### Step 5: User Receives Recommendation
The personalized recommendation is displayed in the Streamlit interface.

## 🔐 Security Best Practices

### API Key Protection

**CRITICAL:** Never commit your API key to the repository.

#### What We Do:
- ✅ Store API key in environment variables only
- ✅ Use `.gitignore` to exclude `.env` files
- ✅ Load API key at runtime from environment

#### What NOT to Do:
- ❌ Never hardcode API keys in Python files
- ❌ Never commit `.env` files to Git
- ❌ Never share your API key in code or documentation

#### Example of Secure Setup:

```bash
# Set API key as environment variable
export OPENAI_API_KEY="your-key-here"

# Run the application
streamlit run app.py
```

The application reads the key from the environment at runtime:
```python
from openai import OpenAI
client = OpenAI()  # Automatically uses OPENAI_API_KEY from environment
```

### .gitignore Configuration

The `.gitignore` file excludes:
```
.env
.env.local
*.pyc
__pycache__/
streamlit.log
.streamlit/
venv/
```

## 🚀 Deployment

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Set API key
export OPENAI_API_KEY="your-key"

# Run the app
streamlit run app.py
```

### AWS EC2 Production Deployment

For detailed AWS EC2 deployment instructions, see [AWS_EC2_Deployment_Guide.md](AWS_EC2_Deployment_Guide.md).

**Quick Summary:**
1. Launch an Ubuntu EC2 instance
2. Clone the repository
3. Create a virtual environment
4. Install dependencies
5. Set the API key as an environment variable
6. Run Streamlit in the background with `nohup`

```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

Access the application at: `http://<EC2-Public-IP>:8501`

## 📊 Monitoring and Logs

### View Real-Time Logs

```bash
tail -f streamlit.log
```

This shows the verbose output of the agents collaborating, including:
- Which agent is working
- What tool they're using
- What decisions they're making
- What context they're passing to the next agent

### Log Example

```
🤖 Crew: crew
  📋 Task: 78df9080-8904-4b02-8bb8-2b31276fb38f
    Status: Executing Task...
    └─ 🔧 Restaurant Search Tool (16)
       Crew: crew
       Task: 78df9080-8904-4b02-8bb8-2b31276fb38f
         Status: Executing Task...
         └─ 🔧 Restaurant Search Tool (17)
```

## 🧪 Testing

### Manual Testing

1. **Test with Simple Query:**
   ```
   "Italian restaurant in New York"
   ```

2. **Test with Complex Query:**
   ```
   "Vegan-friendly, high-end restaurant in San Francisco with a view, suitable for a business dinner"
   ```

3. **Test with Location-Specific Query:**
   ```
   "Affordable local restaurant in Tokyo near Shibuya Station"
   ```

### Expected Output

For each query, you should receive:
- A personalized recommendation with restaurant name
- Explanation of why it matches your criteria
- Details about cuisine, price range, and atmosphere
- Specific reasons why this restaurant is the best choice

## 📖 Documentation

- **[AWS_EC2_Deployment_Guide.md](AWS_EC2_Deployment_Guide.md)** - Complete guide for deploying on AWS EC2
- **[SPEAKER_NOTES.md](SPEAKER_NOTES.md)** - Detailed speaker notes for team presentations
- **[PRESENTATION_SCRIPT.md](PRESENTATION_SCRIPT.md)** - Full word-for-word presentation script with timing

## 🎤 Presentation Materials

This project includes complete presentation materials:

- **Team Presentation:** 3-slide presentation with terminal aesthetic
- **Speaker Notes:** Detailed talking points and explanations
- **Presentation Script:** Word-for-word delivery script with timing

See the `demo_presentation/` folder for the HTML slides.

## 💡 Use Cases

This multi-agent architecture can be adapted for many applications:

- **Content Creation:** Research → Write → Edit
- **Data Analysis:** Collect → Analyze → Report
- **Customer Service:** Understand → Respond → Escalate
- **Code Review:** Analyze → Suggest → Document
- **Market Research:** Research → Analyze → Summarize

## 🔄 Future Enhancements

Potential improvements for future versions:

- [ ] Connect to real restaurant APIs (Google Maps, Yelp, etc.)
- [ ] Add user authentication and history tracking
- [ ] Implement caching to reduce API calls
- [ ] Add support for multiple languages
- [ ] Create a mobile app version
- [ ] Add restaurant image display
- [ ] Implement user ratings and feedback
- [ ] Add dietary restriction filters
- [ ] Create admin dashboard for analytics

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ❓ FAQ

### Q: Why use multiple agents instead of a single model?

**A:** Specialized agents produce better results than a single model trying to do everything. Each agent focuses on one task, making better decisions and producing higher-quality output. The collaboration between agents refines the recommendation at each step.

### Q: How much does this cost?

**A:** Each recommendation costs less than $0.005 (half a cent). This makes it affordable for production use at scale.

### Q: Can I use a different LLM?

**A:** Yes. The code uses OpenAI by default, but you can modify `crew.py` to use other LLMs supported by LangChain (Anthropic, Hugging Face, etc.).

### Q: Is the API key safe?

**A:** Yes, if you follow the security practices outlined in this README. Never commit your API key to Git. Always use environment variables.

### Q: How long does each recommendation take?

**A:** Typically 2-5 seconds, depending on the complexity of the request and OpenAI API latency.

### Q: Can I deploy this on other cloud platforms?

**A:** Yes. The application is containerizable and can be deployed on any platform that supports Python (AWS, Google Cloud, Azure, Heroku, etc.).

## 📞 Support

For issues, questions, or suggestions:

1. Check the [FAQ](#faq) section above
2. Open an issue on GitHub

## 🙏 Acknowledgments

- **CrewAI:** For the powerful multi-agent orchestration framework
- **Streamlit:** For making it easy to build web interfaces
- **OpenAI:** For the gpt-4.1-mini model
- **LangChain:** For excellent LLM integration

## 📈 Project Status

**Status:** ✅ Production Ready

- [x] Core functionality implemented
- [x] Streamlit UI created
- [x] AWS EC2 deployment tested
- [x] Security best practices implemented
- [x] Documentation complete
- [x] Presentation materials ready

---

**Last Updated:** November 2025

**Author:** Siva satya prasad reddy 

**Repository:** [https://github.com/dsspreddy2/crewaitesting](https://github.com/dsspreddy2/crewaitesting)
