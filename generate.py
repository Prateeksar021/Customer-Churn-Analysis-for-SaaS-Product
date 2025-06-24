import pandas as pd
import random
import sqlite3
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

NUM_USERS = 1000
START_DATE = datetime(2025, 6, 21)

plan_types = ['Free', 'Basic', 'Premium']
locations = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Jaipur']
user_base = []

for i in range(NUM_USERS):
    user_id = f"U{1000 + i}"
    name = fake.name()
    senior_citizen = random.choice([0, 1])
    plan_type = random.choice(plan_types)
    location = random.choice(locations)
    user_base.append({
        'user_id': user_id,
        'user_name': name,
        'senior_citizen': senior_citizen,
        'plan_type': plan_type,
        'location': location
    })

def generate_day_activity(day_offset, user_base, churned_users=set()):
    date = START_DATE + timedelta(days=day_offset)
    data = []
    for user in user_base:
        if user['user_id'] in churned_users:
            is_active = 0
            session_count = 0
        else:
            is_active = random.choices([1, 0], weights=[0.9, 0.1])[0]
            session_count = random.randint(1, 10) if is_active else 0
        data.append({
            **user,
            'session_count': session_count,
            'last_login': date.strftime('%Y-%m-%d'),
            'is_active': is_active
        })
    return pd.DataFrame(data)

day1_df = generate_day_activity(0, user_base)
churned_day2 = set(random.sample([u['user_id'] for u in user_base], k=int(0.1 * NUM_USERS)))
day2_df = generate_day_activity(1, user_base, churned_users=churned_day2)
churned_day3 = churned_day2.union(set(random.sample([u for u in [u['user_id'] for u in user_base] if u not in churned_day2], k=int(0.05 * NUM_USERS))))
day3_df = generate_day_activity(2, user_base, churned_users=churned_day3)

day1_df.to_csv("user_activity_day1.csv", index=False)
day2_df.to_csv("user_activity_day2.csv", index=False)
day3_df.to_csv("user_activity_day3.csv", index=False)
