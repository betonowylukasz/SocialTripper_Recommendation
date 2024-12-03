import pandas as pd
import random
import json

# Wczytanie danych użytkowników z pliku JSON
with open("final_users.json", "r") as f:
    user_data = pd.DataFrame(json.load(f))

# Liczba par do wygenerowania
num_pairs = 250  # Możesz dostosować tę liczbę do swoich potrzeb

# Lista przechowująca dane testowe
test_data = []

for _ in range(num_pairs):
    # Losowe wybieranie dwóch różnych użytkowników z danych
    user1 = user_data.sample().iloc[0]
    user2 = user_data.sample().iloc[0]

    # Sprawdzenie, czy są to różni użytkownicy
    while user1['name'] == user2['name']:
        user2 = user_data.sample().iloc[0]

    # Generowanie losowego recommendation score
    recommendation_score = round(random.uniform(0, 1), 2)  # Skala 0–1, zaokrąglona do 2 miejsc

    # Tworzenie rekordu testowego z cechami obu użytkowników
    test_record = {
        "name_1": user1['name'],
        "name_2": user2['name'],

        # Cechy użytkownika 1
        "age_user1": user1['age'],
        "age_user2": user2['age'],
        "bmi_user1": user1['bmi'],
        "bmi_user2": user2['bmi'],
        "location_user1": user1['location'],
        "location_user2": user2['location'],
        "gender_user1": user1['gender'],
        "gender_user2": user2['gender'],
        'activities_user1': user1['activity_type'],
        'activities_user2': user2['activity_type'],
        'avg_time_user1': user1['avg_time'],
        'avg_time_user2': user2['avg_time'],

        "recommendation_score": recommendation_score
    }

    # Dodawanie rekordu do listy testowej
    test_data.append(test_record)

# Konwersja do DataFrame i zapis do CSV
test_df = pd.DataFrame(test_data)
test_df.to_csv("generated_test_data.csv", index=False)

print("Dane testowe zostały wygenerowane i zapisane do pliku 'generated_test_data.csv'")
