import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# # Wczytanie danych z pliku JSON
# with open("activities_with_age.json", "r") as file:
#     user_data = json.load(file)
#
# # Zbiór do przechowywania unikalnych aktywności
# unique_activities = set()
#
# # Iteracja po każdym użytkowniku i dodanie aktywności do zbioru
# for user in user_data:
#     activities = user.get("activity_type", [])
#     unique_activities.update(activities)
#
# # Konwersja zbioru na listę i sortowanie alfabetyczne
# unique_activities = sorted(unique_activities)
#
# # Wyświetlenie unikalnych aktywności
# print("Unikalne rodzaje aktywności:")
# for activity in unique_activities:
#     print(activity)
#
# # Definicja mapowania aktywności do nowych kategorii
# activity_mapping = {
#     "Tennis": "Sport",
#     "Golf": "Sport",
#     "Gravel Ride": "Ride",
#     "Mountain Bike Ride": "Ride",
#     "E-Bike Ride": "Ride",
#     "E-Mountain Bike Ride": "Ride",
#     "Kayaking": "Water Activities",
#     "Kitesurf": "Water Activities",
#     "Rowing": "Water Activities",
#     "Swim": "Water Activities",
#     "Trail Run": "Run",
#     "Windsurf": "Water Activities",
#     "Workout": "Camping",
# }
#
# # Przetworzenie każdej aktywności zgodnie z mapowaniem
# for user in user_data:
#     user["activity_type"] = [
#         activity_mapping.get(activity, activity)  # Zamiana aktywności lub pozostawienie oryginalnej
#         for activity in user.get("activity_type", [])
#     ]
#     if user["activity_type"] == ["Camping"]: user["avg_time"] = user["avg_time"] * 5
#
# # Zapisanie zmodyfikowanych danych z powrotem do pliku JSON
# with open("final_users.json", "w") as file:
#     json.dump(user_data, file, indent=4)
#
# print("Aktywności zostały zamienione zgodnie z mapowaniem.")

with open('final_users.json', 'r') as f:
    data = json.load(f)

# Zliczanie aktywności
activity_counter = Counter()

# Przechodzenie po użytkownikach i zliczanie każdej aktywności
for user in data:
    activities = user.get("activity_type", [])
    activity_counter.update(activities)

# Wyświetlenie liczby każdej aktywności
for activity, count in activity_counter.items():
    print(f"{activity}: {count}")
