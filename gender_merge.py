import json
import glob
import re
from collections import defaultdict
import random

from genderize import Genderize
import requests
import time

# def get_gender(name):
#     url = f"https://api.genderize.io/?name={name}"
#     time.sleep(0.5)
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("gender")  # Zwraca 'male', 'female' lub None
#     return None


def get_gender_namsor(name, retries):
    url = f"https://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/{name}"
    time.sleep(1)
    headers = {
        "X-API-KEY": '1519b877e43a6045b70eec5fca8e0857',
        "Accept": "application/json",
    }

    for attempt in range(retries):
        try:
            # Ustaw timeout na 10 sekund
            response = requests.request("GET", url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("likelyGender")
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None

        except requests.exceptions.ConnectTimeout:
            print(f"Connection timed out. Retrying... (Attempt {attempt + 1} of {retries})")
            time.sleep(5)  # Czeka 5 sekund przed ponowną próbą

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    print("Failed to connect after multiple attempts.")
    return None

def time_to_seconds(time_str):
    hours, minutes, seconds = 0, 0, 0
    # Wyszukaj godziny, minuty i sekundy
    h_match = re.search(r'(\d+)h', time_str)
    m_match = re.search(r'(\d+)m', time_str)
    s_match = re.search(r'(\d+)s', time_str)

    if h_match:
        hours = int(h_match.group(1))
    if m_match:
        minutes = int(m_match.group(1))
    if s_match:
        seconds = int(s_match.group(1))

    # Zamień wszystko na sekundy
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def clean_name(name):
    cleaned_name = re.sub(r'[^A-Za-z0-9\s\-\(\)\'\"_,.]', '', name)
    return cleaned_name.strip()

# Lista przechowująca wszystkie aktywności
all_activities = []

# Iterujemy po wszystkich plikach JSON o nazwach activities_data1.json do activities_data12.json
for i in range(1, 19):
    filename = f"activities_data{i}.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            # Wczytaj zawartość pliku JSON
            data = json.load(file)
            # Dodaj zawartość do listy all_activities
            all_activities.extend(data)
            print(f"Wczytano dane z {filename}")
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony. Pomijam ten plik.")
    except json.JSONDecodeError:
        print(f"Plik {filename} nie zawiera poprawnych danych JSON. Pomijam ten plik.")

# Zapisz wszystkie aktywności do jednego dużego pliku JSON
with open("merged_activities_data.json", "w", encoding="utf-8") as output_file:
    json.dump(all_activities, output_file, ensure_ascii=False, indent=4)

with open("merged_activities_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Usuń aktywności, gdzie 'location' jest None lub nie istnieje
filtered_data = [activity for activity in data if activity.get("location") is not None]

# Zapisz przefiltrowane dane do pliku (możesz nadpisać plik lub zapisać w nowym pliku)
with open("filtered_activities_data.json", "w", encoding="utf-8") as output_file:
    json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

with open("filtered_activities_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Przekształć lokalizację, aby zawierała tylko kraj
for activity in data:
    location = activity.get("location")
    if location:
        if "Voivodeship" in location:
            activity["location"] = "Poland"
        else:
            # Kraj jest ostatnim elementem po przecinku, po usunięciu początkowego "· " i białych znaków
            country = location.split(",")[-1].strip()
            activity["location"] = country

# Zapisz wynik do nowego pliku
with open("filtered_activities_data.json", "w", encoding="utf-8") as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

with open("filtered_activities_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Słownik do grupowania aktywności według użytkowników
user_activities = defaultdict(lambda: {"activity_type": set(), "time": []})

# Przetwórz dane
for activity in data:
    name = activity.get("name")
    location = activity.get("location")
    activity_type = activity.get("activity_type")
    time_str = activity.get("time")

    name = clean_name(name)

    if name and activity_type and time_str:
        user_activities[name]["location"] = location
        gender = get_gender_namsor(name, 5)
        print(f"Name: {name}, Gender: {gender}")
        user_activities[name]["gender"] = gender
        user_activities[name]["activity_type"].add(activity_type)
        # Konwertuj czas na sekundy i dodaj do listy czasów użytkownika
        user_activities[name]["time"].append(time_to_seconds(time_str))

# Przekształć dane na listę i oblicz średnią czasu dla każdego użytkownika
result_data = []
for name, info in user_activities.items():
    avg_time = sum(info["time"]) / len(info["time"]) if info["time"] else 0
    result_data.append({
        "name": name,
        "location": info["location"],
        "gender": info["gender"],
        "activity_type": list(info["activity_type"]),  # Zamień zestaw na listę
        "avg_time": avg_time
    })

# Zapisz wynik do nowego pliku
with open("combined_user_activities.json", "w", encoding="utf-8") as output_file:
    json.dump(result_data, output_file, ensure_ascii=False, indent=4)