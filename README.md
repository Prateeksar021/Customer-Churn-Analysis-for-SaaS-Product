# SaaS Customer Churn Analysis Dashboard

This project was built for the **Onelogica BI Internship Challenge** using the "Customer Churn Analysis for a SaaS Product" use case. It simulates a real-world data pipeline and presents business insights to help reduce customer churn.

---

## Project Overview

The objective is to simulate and analyze user behavior over 3 days for a SaaS product. The insights help the Customer Success team identify user churn, trends, and actionable strategies to improve retention.

---

## Use Case: Customer Churn Analysis for a SaaS Product

- Daily user activity logs are simulated for 3 consecutive days.
- ETL pipeline loads and updates records using CDC (Change Data Capture).
- A star schema is designed for dimensional analysis.
- A Streamlit dashboard presents the data insights interactively.

---
📁 Churn_Analysis/
├──Scripts
       └── user_activity_day1.csv
       ├── user_activity_day2.csv
       ├── user_activity_day3.csv
       ├── generate.py
       ├── etl_pipeline.py
       ├── Main.py
├── etl.log
├── user_activity.db
└── README.md


---

## ⚙️ How to Run This Project

### ✅ Step 1: Clone the Repo

```bash
git clone https://github.com/your-username/saas-churn-analysis.git
cd saas-churn-analysis

# Step 2: Install Requirements
pip install -r requirements.txt

# Step 3: Run the Dashboard
enter on bash
streamlit run Main.py

# Dashboard Features
KPIs: Total users, Active users, Churned users, Senior citizens

Churn Pie Chart: Shows churn rate visually

Avg. Session Count by Plan & Location

User Retention Trend over 3 days

Recommendations Panel with actionable churn reduction strategies

# Insights Generated
Premium users have higher engagement than Free/Basic plans.

Certain locations show lower usage and higher churn.

~15% churn was observed on the final day.

Senior citizens contribute to a smaller but notable segment (~10–12%).

# Recommendations to Reduce Churn
Boost Free/Basic Plan Engagement: Offer onboarding tutorials and guided tours.

Location-Based Offers: Target low-usage regions with incentives.

Re-engage Inactive Users: Automate win-back emails or SMS.

Senior Citizen UX Improvements: Improve accessibility and customer support.

Behavioral Analytics: Monitor drop-offs and trigger personalized nudges.

# Tech Stack
Python, Pandas, SQLite

Matplotlib, Seaborn

Streamlit (for interactive BI Dashboard)

Faker (to generate synthetic user data)




