# Customer Churn Analysis with Dashboard
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load CSVs
file_day1 = "user_activity_day1.csv"
file_day2 = "user_activity_day2.csv"
file_day3 = "user_activity_day3.csv"

# Load Data
@st.cache_data
def load_data():
    day1 = pd.read_csv(file_day1)
    day2 = pd.read_csv(file_day2)
    day3 = pd.read_csv(file_day3)
    day1['day'] = 'Day 1'
    day2['day'] = 'Day 2'
    day3['day'] = 'Day 3'
    return pd.concat([day1, day2, day3], ignore_index=True), day1, day2, day3

df_all, day1, day2, day3 = load_data()
df_all['last_login'] = pd.to_datetime(df_all['last_login'])

# Churn Calculation
latest_df = day3
churned_users = latest_df[latest_df['is_active'] == 0]['user_id'].unique()
total_users = latest_df['user_id'].nunique()
churned = len(churned_users)
active = total_users - churned
churn_rate = round((churned / total_users) * 100, 2)

# Senior Citizens
senior_citizens = latest_df[latest_df['senior_citizen'] == 1].shape[0]

# Group Stats
by_plan = latest_df.groupby('plan_type')['session_count'].mean().reset_index()
by_location = latest_df.groupby('location')['session_count'].mean().reset_index()
trend = df_all.groupby('day')['session_count'].mean().reset_index()

# Retention
d1_active = set(day1[day1['is_active'] == 1]['user_id'])
d2_active = set(day2[day2['is_active'] == 1]['user_id'])
d3_active = set(day3[day3['is_active'] == 1]['user_id'])
retention = {
    "Day 1 only": len(d1_active - d2_active - d3_active),
    "Day 1 & 2": len(d1_active & d2_active - d3_active),
    "Day 1 & 3": len(d1_active & d3_active - d2_active),
    "All 3 Days": len(d1_active & d2_active & d3_active)
}

# Streamlit Dashboard
st.set_page_config(page_title="SaaS Churn Dashboard", layout="wide")
st.title("SaaS Product - Customer Churn Analysis")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", total_users)
col2.metric("Active Users", active)
col3.metric("Churned Users", churned)
col4.metric("Senior Citizens", senior_citizens)

# Churn Rate Pie
fig1, ax1 = plt.subplots()
ax1.pie([active, churned], labels=['Active', 'Churned'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax1.set_title('Churn Rate')
st.pyplot(fig1)

# Avg Session by Plan
fig2, ax2 = plt.subplots()
sns.barplot(data=by_plan, x='plan_type', y='session_count', palette='Blues', ax=ax2)
ax2.set_title('Avg Session by Plan Type')
st.pyplot(fig2)

# Avg Session by Location
fig3, ax3 = plt.subplots()
sns.barplot(data=by_location, x='location', y='session_count', palette='Oranges', ax=ax3)
ax3.set_title('Avg Session by Location')
st.pyplot(fig3)

# Usage Trend
fig4, ax4 = plt.subplots()
sns.lineplot(data=trend, x='day', y='session_count', marker='o', ax=ax4)
ax4.set_title('Average Session Trend Over Days')
st.pyplot(fig4)

# Retention Summary
st.subheader("Retention Summary")
st.write(retention)

# Recommendations
st.markdown("""
### 💡 Recommendations to Reduce Churn:
- Improve engagement for users on Free/Basic plans with onboarding tutorials.
- Target users in lower activity locations (e.g., with emails, push notifications).
- Design personalized offers for senior citizens based on feedback.
- Re-engage users inactive for 2+ days with win-back campaigns.
- Monitor plan usage drops and suggest upgrades/downgrades timely.
""")
