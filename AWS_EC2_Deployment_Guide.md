# AWS EC2 Deployment Guide for CrewAI Restaurant Recommender

This guide provides step-by-step instructions for deploying the **CrewAI Restaurant Recommender** Streamlit application on an AWS EC2 instance running Ubuntu.

## Prerequisites

1.  An active AWS account.
2.  An EC2 instance (e.g., t2.micro or t3.micro) running **Ubuntu 22.04 LTS** or later.
3.  A security group configured to allow inbound traffic on:
    *   **Port 22 (SSH):** For connecting to the instance.
    *   **Port 8501 (Custom TCP):** The default port for Streamlit applications.
4.  The application code (`app.py`, `crew.py`, `requirements.txt`).

## Step 1: Connect to the EC2 Instance

Connect to your EC2 instance using SSH and your private key.

\`\`\`bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
\`\`\`

## Step 2: Install Dependencies

Update the package list and install Python and necessary tools.

\`\`\`bash
sudo apt update
sudo apt install -y python3 python3-pip git
\`\`\`

## Step 3: Clone the Application

Clone your application code (assuming you have pushed it to a repository, or manually transfer the files).

**Option A: Using Git (Recommended)**

\`\`\`bash
git clone <your-repo-url>
cd <your-repo-directory>
\`\`\`

**Option B: Manual File Transfer (If using the provided files)**

Create the project directory and transfer the files using `scp` from your local machine, or manually create them on the EC2 instance.

\`\`\`bash
mkdir restaurant_crew_app
cd restaurant_crew_app
# Manually create or transfer app.py, crew.py, and requirements.txt
\`\`\`

## Step 4: Install Python Requirements

Install the required Python libraries, including `crewai`, `streamlit`, and `openai`.

\`\`\`bash
pip3 install -r requirements.txt
\`\`\`

## Step 5: Set Environment Variables

The application requires the OpenAI API key. **For the demo, you must set your own `OPENAI_API_KEY`**.

\`\`\`bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
# To make this permanent, add the line above to the end of your ~/.bashrc file.
\`\`\`

## Step 6: Run the Streamlit Application

Run the Streamlit application. We will use the `nohup` command to keep the application running even after you close the SSH session.

\`\`\`bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
\`\`\`

*   `--server.port 8501`: Specifies the port.
*   `--server.address 0.0.0.0`: Makes the application accessible from the public internet.
*   `nohup ... &`: Runs the process in the background and prevents it from being terminated when you log out.
*   `> streamlit.log 2>&1`: Redirects all output (stdout and stderr) to a log file.

## Step 7: Access the Application

The application is now running. You can access it by navigating to your EC2 instance's public IP address and the Streamlit port in your web browser:

\`\`\`
http://your-ec2-public-ip:8501
\`\`\`

To stop the application, you can find the process ID (PID) and kill it:

\`\`\`bash
pgrep -f "streamlit run"
# Example: kill 12345
kill <PID>
\`\`\`

## Step 8: Demo Presentation Notes

*   **Highlight the Multi-Agent System:** Explain the roles of the **Researcher**, **Analyzer**, and **Generator** agents.
*   **Show the Code:** Briefly show `crew.py` to demonstrate the CrewAI setup (Agents, Tasks, Crew).
*   **Show the UI:** Demonstrate `app.py` to show how Streamlit provides a simple, interactive interface.
*   **Emphasize Cost-Effectiveness:** Mention the use of the pre-configured `gpt-4.1-mini` model to keep token usage and cost low for a functional demo.
*   **Show the Log:** If possible, show the `streamlit.log` file on the EC2 instance to demonstrate the verbose collaboration log of the agents.

\`\`\`bash
tail -f streamlit.log
\`\`\`
