from bs4 import BeautifulSoup
import requests
import json


# Wczytaj zapisany plik HTML
with open("strava_activity_page18.html", "r", encoding="utf-8") as file:
    page_source = file.read()

# Tworzymy obiekt BeautifulSoup z wczytanego HTML
soup = BeautifulSoup(page_source, "html.parser")

activities_data = []

# Przykładowe dane, które chcemy wydobyć:
activities = soup.find_all("div", class_="------packages-feed-ui-src-components-media-Card-Card__feed-entry--WKvAQ ------packages-feed-ui-src-components-media-Card-Card__card--dkL_L")

# Iterujemy po aktywnościach
for activity in activities:
    try:
        name_tag = activity.find("a", {"data-testid": "owners-name"})
        name = name_tag.get_text(strip=True) if name_tag else None

        profile_picture_tag = activity.find("img", {"title": name})  # Wyszukiwanie na podstawie tytułu jako imienia
        if profile_picture_tag:
            profile_picture = profile_picture_tag["src"].replace("medium", "large")
        else:
            profile_picture = None

        location_tag = activity.find("div", {"data-testid": "location"})
        location = location_tag.get_text(strip=True) if location_tag else None

        activity_type_tag = activity.find("svg", class_="------packages-feed-ui-src-features-Activity-Activity__activity-icon--lq3sA")
        if activity_type_tag:
            activity_type = activity_type_tag.find("title").get_text(strip=True) if activity_type_tag.find(
                "title") else None
        else:
            activity_type = None

        distance = None
        time = None
        stats = activity.find_all("div", class_="------packages-ui-Stat-Stat-module__stat--Y2ZBX")
        for stat in stats:
            label = stat.find("span", class_="------packages-ui-Stat-Stat-module__statLabel--tiWBB")
            value_tag = stat.find("div", class_="------packages-ui-Stat-Stat-module__statValue--phtGK")

            if label and value_tag:
                stat_value = value_tag.get_text(strip=True)
                if label.get_text(strip=True) == "Distance":
                    distance = stat_value
                elif label.get_text(strip=True) == "Time":
                    time = stat_value

        activities_data.append({
            "name": name,
            "profile_picture": profile_picture,
            "location": location,
            "activity_type": activity_type,
            "distance": distance,
            "time": time
        })

        # Wyświetlamy wyniki
        print(f"Imię i nazwisko: {name}")
        print(f"Zdjęcie profilowe: {profile_picture}")
        print(f"Lokacja: {location}")
        print(f"Rodzaj aktywności: {activity_type}")
        print(f"Dystans: {distance}")
        print(f"Czas trwania: {time}")
        # print("-" * 40)

    except AttributeError as e:
        print(f"Nie udało się znaleźć niektórych danych: {e}")
        print("-" * 40)

with open("activities_data18.json", "w", encoding="utf-8") as json_file:
    json.dump(activities_data, json_file, ensure_ascii=False, indent=4)

print("Dane zostały zapisane do pliku activities_data1.json")