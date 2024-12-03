import pandas as pd
from gensim.models import KeyedVectors
import numpy as np

# Ścieżka do pliku age_data.csv
age_data_file = "age_data.csv"  # Zmień na rzeczywistą ścieżkę do pliku

# Wczytanie danych
age_data = pd.read_csv(age_data_file)

# Ścieżka do pliku glove.6B.300d.txt
glove_file = "glove.6B.50d.txt"  # Zmień na rzeczywistą ścieżkę do pliku

# Wczytanie modelu GloVe
model = KeyedVectors.load_word2vec_format(glove_file, binary=False, no_header=True)


# Funkcja do przekształcania nazw krajów i sprawdzania dostępności w GloVe
def get_country_embedding(country_name):
    words = country_name.lower().split()  # Dzielimy kraj na słowa
    embeddings = []

    for word in words:
        if word in model:
            embeddings.append(model[word])

    if embeddings:
        # Jeżeli wszystkie słowa są dostępne w modelu, zwróć średnią z ich embeddingów
        return np.mean(embeddings, axis=0)
    else:
        # Jeżeli nie ma embeddingu, zwróć None (możesz to później obsłużyć)
        return None


# Wyodrębnienie nazw krajów z pliku CSV
countries_from_file = age_data['country'].tolist()

# Uzyskanie embeddingów dla krajów
country_embeddings = {}

for country in countries_from_file:
    embedding = get_country_embedding(country)
    if embedding is not None:
        country_embeddings[country] = embedding
    else:
        print(f"Brak embeddingu dla kraju: {country}")

# Wyświetlenie wyników
print(country_embeddings)

embedding_csv_file = "country_embeddings.csv"

# Tworzenie DataFrame z embeddingami
embedding_df = pd.DataFrame.from_dict(country_embeddings, orient="index")

# Dodanie nazw krajów jako kolumny
embedding_df.reset_index(inplace=True)
embedding_df.columns = ["country"] + [f"dim_{i}" for i in range(embedding_df.shape[1] - 1)]

# Zapis do CSV
embedding_df.to_csv(embedding_csv_file, index=False)
print(f"Embeddingi zapisane do pliku: {embedding_csv_file}")
