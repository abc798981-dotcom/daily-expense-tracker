🧠 AI Expense Intelligence Dashboard
A modern, high-tech financial tracking application built with Python, Streamlit, and Machine Learning. This tool doesn't just record what you spend—it uses ARIMA Time-Series Forecasting to predict your future spending and helps you manage your daily budget in real-time.

🚀 Key Features
Real-Time Tracking: Log daily expenses with descriptions and categories via an intuitive sidebar.

Intelligent Budgeting: Automatically calculates your Daily Allowance based on how many days are left in the month and your remaining balance.

AI Forecasting: Uses an ARIMA (AutoRegressive Integrated Moving Average) model to analyze historical trends and predict next month's total expenditure.

Visual Analytics: Interactive doughnut and bar charts powered by Plotly to visualize spending proportions.

Dynamic Alerts: Visual "Over-Limit" warnings trigger automatically when you cross 85% of your monthly budget.

Financial Guardrails: Provides a suggested 50/30/20 (Essentials/Wants/Savings) allocation based on your specific salary.

🛠️ Tech Stack
Frontend: Streamlit (Python-based Web Framework)

Data Processing: Pandas, NumPy

Machine Learning: Statsmodels (ARIMA Model)

Visualizations: Plotly Express

Deployment: Cloudflare Tunnel (for secure public access from Google Colab)

📋 Installation & Usage
Running on Google Colab (Recommended)
This application is optimized for Google Colab. Follow these steps:

Install Dependencies:

Python
!pip install streamlit statsmodels plotly --quiet
Setup Cloudflare Tunnel:
Download the cloudflared binary to create a public link for the Streamlit server.

Execute app.py:
Run the cell containing the %%writefile app.py command to save the code.

Launch:
Run the launcher cell to start the Streamlit server and click the generated trycloudflare.com link.

Running Locally
Clone the Repository:

Bash
git clone https://github.com/yourusername/ai-expense-tracker.git
cd ai-expense-tracker
Install Requirements:

Bash
pip install -r requirements.txt
Run the App:

Bash
streamlit run app.py
📉 How the AI Works
The system utilizes the ARIMA(1, 1, 1) model. It treats your historical monthly spending as a stationary time series, calculating:

AR (Autoregressive): Relationship between an observation and a number of lagged observations.

I (Integrated): Differencing of raw observations to make the time series stationary.

MA (Moving Average): Relationship between an observation and a residual error from a moving average model.

This allows the dashboard to warn you before you overspend next month based on your current trajectory.
