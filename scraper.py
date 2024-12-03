from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ścieżka do ChromeDriver
driver_path = "D:/workspace/algorytm_rekomendacji/chromedriver.exe"

# Ścieżka do Chrome na dysku C
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Podaj ścieżkę do nowej wersji Chrome

# Skonfiguruj opcje Chrome, ustawiając ścieżkę do nowej przeglądarki
chrome_options = Options()
chrome_options.binary_location = chrome_path

# Utwórz obiekt Service i przekaż go do Chrome WebDriver wraz z opcjami
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Otwórz stronę logowania do Stravy
driver.get("https://www.strava.com/login")

try:
    # Czekaj, aż pole e-mail będzie widoczne
    email_field = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    password_field = driver.find_element(By.ID, "password")

    # Wprowadź swoje dane
    email_field.send_keys("266542@student.pwr.edu.pl")  # Podaj swój email
    password_field.send_keys("On@9P0w.s")  # Podaj swoje hasło
    password_field.send_keys(Keys.RETURN)  # Naciśnij Enter, aby zalogować się

    # Odczekaj chwilę, aby upewnić się, że logowanie jest zakończone
    time.sleep(5)  # Możesz dostosować czas w razie potrzeby

    # Po zalogowaniu przejdź do strony z aktywnościami klubu
    driver.get("https://www.strava.com/clubs/605991/recent_activity?num_entries=200")

    # Pobierz HTML strony
    page_source = driver.page_source

    with open("strava_activity_page18.html", "w", encoding="utf-8") as file:
        file.write(page_source)
    print("HTML zapisano do pliku 'strava_activity_page1.html'.")

finally:
    # Zamknij przeglądarkę po zakończeniu
    driver.quit()
