import json
import pandas as pd
import random
import numpy as np

# Wczytanie danych BMI z pliku CSV
bmi_df = pd.read_csv('bmi_data.csv', skiprows=4)  # Pomijamy pierwsze 4 wiersze metadanych
bmi_df.columns = ["Country", "Male", "Female"]

print(bmi_df)

# Wczytanie danych aktywności z pliku JSON
with open('combined_user_activities.json', 'r') as f:
    activities = json.load(f)


# Funkcja generująca BMI z rozkładem normalnym
def get_bmi_for_country_and_gender(country, gender):
    row = bmi_df[bmi_df["Country"] == country]
    if row.empty:
        return None  # Brak danych dla danego kraju

    bmi_range = row[gender].values[0]
    if pd.isnull(bmi_range):
        return None  # Brak danych dla danej płci

    bmi_mean = bmi_range.split()[0]
    bmi_value = np.clip(np.random.normal(float(bmi_mean), 4), 13, 45)
    return round(float(bmi_value), 1)


# Dodanie BMI do aktywności
for activity in activities:
    country = activity.get("location")
    gender = activity.get("gender")

    if not country or not gender:
        continue

    # Przypisanie płci do odpowiedniego formatu
    gender_key = "Male" if gender.lower() == "male" else "Female"
    bmi = get_bmi_for_country_and_gender(country, gender_key)

    activity["bmi"] = bmi


# Zapis wyników do nowego pliku JSON
with open('activities_with_bmi.json', 'w') as f:
    json.dump(activities, f, indent=4)
