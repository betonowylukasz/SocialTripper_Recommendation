import pandas as pd
import numpy as np
import json

# Wczytanie pliku CSV z medianami wieku
age_data = pd.read_csv('age_data.csv')  # Uzupełnij nazwę pliku
print(age_data.columns)
age_data.set_index("country", inplace=True)

# Wczytanie danych użytkowników
with open('activities_with_bmi.json', 'r') as file:
    user_data = json.load(file)


# Funkcja generująca wiek na podstawie mediany i płci
def generate_age(country, gender):
    if country in age_data.index:
        if gender.lower() == 'male':
            median_age = age_data.loc[country, 'MedianAge2023Male']
        else:
            median_age = age_data.loc[country, 'MedianAge2023Female']

        # Generowanie wieku z rozkładu normalnego, przy dolnym i górnym limicie 13 i 80 lat
        age = np.clip(np.random.normal(median_age, 7), 13, 80)
        return int(age)
    else:
        return None


# Przypisanie wieku do każdej aktywności
for activity in user_data:
    country = activity.get('location')
    gender = activity.get('gender')
    activity['age'] = generate_age(country, gender)

with open('activities_with_age.json', 'w') as file:
    json.dump(user_data, file, indent=4)
