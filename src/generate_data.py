import pandas as pd
import numpy as np

np.random.seed(42)

number_of_cows = 100

cow_ids = [f"C{i:04d}" for i in range(1, number_of_cows + 1)]

breeds = np.random.choice(
    ["Holstein", "Jersey", "Brown Swiss"],
    size=number_of_cows,
    p=[0.70, 0.20, 0.10]
)

lactation_numbers = np.random.randint(
    1,
    6,
    size=number_of_cows
)

cow_master = pd.DataFrame({
    "cow_id": cow_ids,
    "breed": breeds,
    "lactation_number": lactation_numbers
})

print(cow_master.head())

# Save the DataFrame as a CSV file
cow_master.to_csv(
    "data/raw/cow_master.csv",
    index=False
)

print("cow_master.csv created successfully!")

# -----------------------------------
# Generate milk production data
# -----------------------------------

dates = pd.date_range(
    start="2026-01-01",
    periods=90,
    freq="D"
)

milk_records = []

for cow_id in cow_ids:

    # Each cow has a slightly different normal milk production
    baseline_milk = np.random.normal(
        loc=32,
        scale=5
    )

    for date in dates:

        # Daily production varies slightly
        daily_milk = baseline_milk + np.random.normal(
            loc=0,
            scale=2
        )

        milk_records.append({
            "cow_id": cow_id,
            "date": date,
            "milk_kg": round(max(daily_milk, 0), 2)
        })

milk_production = pd.DataFrame(milk_records)

# -----------------------------------
# Introduce intentional data problems
# -----------------------------------

# 1. Add duplicate records
duplicate_rows = milk_production.sample(
    20,
    random_state=42
)

milk_production = pd.concat(
    [milk_production, duplicate_rows],
    ignore_index=True
)


# 2. Add missing cow IDs
missing_id_rows = milk_production.sample(
    10,
    random_state=10
).index

milk_production.loc[
    missing_id_rows,
    "cow_id"
] = None


# 3. Add impossible negative milk values
negative_milk_rows = milk_production.sample(
    10,
    random_state=20
).index

milk_production.loc[
    negative_milk_rows,
    "milk_kg"
] = -10


# 4. Add cow IDs that don't exist in cow_master
unknown_cow_rows = milk_production.sample(
    10,
    random_state=30
).index

milk_production.loc[
    unknown_cow_rows,
    "cow_id"
] = "C9999"

print("\nMilk Production:")
print(milk_production.head())

milk_production.to_csv(
    "data/raw/milk_production.csv",
    index=False
)

print("milk_production.csv created successfully!")

# -----------------------------------
# Generate activity / sensor data
# -----------------------------------

activity_records = []

for cow_id in cow_ids:

    for date in dates:

        # Simulate daily movement
        steps = int(
            np.random.normal(
                loc=4500,
                scale=800
            )
        )

        # Simulate daily rumination time
        rumination_minutes = int(
            np.random.normal(
                loc=450,
                scale=50
            )
        )

        activity_records.append({
            "cow_id": cow_id,
            "date": date,
            "steps": max(steps, 0),
            "rumination_minutes": max(rumination_minutes, 0)
        })


activity = pd.DataFrame(activity_records)

# -----------------------------------
# Introduce activity data problems
# -----------------------------------

# Missing sensor readings
missing_activity_rows = activity.sample(
    15,
    random_state=50
).index

activity.loc[
    missing_activity_rows,
    "steps"
] = np.nan


# Unrealistic activity values
extreme_activity_rows = activity.sample(
    10,
    random_state=60
).index

activity.loc[
    extreme_activity_rows,
    "steps"
] = 50000


# Missing rumination readings
missing_rumination_rows = activity.sample(
    10,
    random_state=70
).index

activity.loc[
    missing_rumination_rows,
    "rumination_minutes"
] = np.nan

print("\nActivity Data:")
print(activity.head())

activity.to_csv(
    "data/raw/activity.csv",
    index=False
)

print("activity.csv created successfully!")

# -----------------------------------
# Generate health event data
# -----------------------------------

health_event_types = [
    "health_check",
    "treatment",
    "vaccination"
]

health_records = []

number_of_health_events = 300

for event_number in range(1, number_of_health_events + 1):

    cow_id = np.random.choice(cow_ids)
    event_date = np.random.choice(dates)
    event_type = np.random.choice(health_event_types)

    health_records.append({
        "event_id": f"E{event_number:04d}",
        "cow_id": cow_id,
        "event_date": event_date,
        "event_type": event_type
    })


health_events = pd.DataFrame(health_records)

# -----------------------------------
# Introduce health event data problems
# -----------------------------------

# Unknown cow IDs
unknown_health_rows = health_events.sample(
    5,
    random_state=80
).index

health_events.loc[
    unknown_health_rows,
    "cow_id"
] = "C9999"


# Missing event types
missing_event_rows = health_events.sample(
    5,
    random_state=90
).index

health_events.loc[
    missing_event_rows,
    "event_type"
] = None


# Add duplicate events
duplicate_health_events = health_events.sample(
    5,
    random_state=100
)

health_events = pd.concat(
    [health_events, duplicate_health_events],
    ignore_index=True
)

print("\nHealth Events:")
print(health_events.head())


health_events.to_csv(
    "data/raw/health_events.csv",
    index=False
)

print("health_events.csv created successfully!")

