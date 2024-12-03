import numpy as np
import pandas as pd
import random
import json
import torch
from sklearn.preprocessing import StandardScaler
from model import MLPModel
from joblib import load

embeddings = 50

with open("final_users.json", "r") as f:
    user_data = pd.DataFrame(json.load(f))

test_data = []

for i in range(len(user_data)):
    user = user_data.iloc[i]

    test_record = {
        "name_1": 'Łukasz Wasilewski',
        "name_2": user['name'],

        # Cechy użytkownika 1 i 2
        "age_user1": 22,
        "age_user2": user['age'],
        "bmi_user1": 20.0,
        "bmi_user2": user['bmi'],
        "location_user1": 'Poland',
        "location_user2": user['location'],
        "gender_user1": 'male',
        "gender_user2": user['gender'],
        'activities_user1': ['Walk', 'Hike'],
        'activities_user2': user['activity_type'],
    }

    test_data.append(test_record)

dataset = pd.DataFrame(test_data)
#dataset.to_csv("wasilewski.csv", index=False)
df = dataset.copy()

embedding_df = pd.read_csv('country_embeddings.csv')

# Przywrócenie embeddingów do słownika
country_embeddings = {
    row["country"]: row.iloc[1:].values.astype(float)
    for _, row in embedding_df.iterrows()
}

def map_location_to_embedding(country_name, country_embeddings):
    return country_embeddings.get(country_name)

def transform_user_data(user_data, country_embeddings, embeddings_range=embeddings):
    # Dodanie nowych kolumn z embeddingami dla location_user1 i location_user2
    user_data['embedding_user1'] = user_data['location_user1'].apply(
        lambda x: map_location_to_embedding(x, country_embeddings)
    )
    user_data['embedding_user2'] = user_data['location_user2'].apply(
        lambda x: map_location_to_embedding(x, country_embeddings)
    )

    # Rozbicie embeddingów na osobne kolumny i obliczenie różnic
    for i in range(embeddings_range):
        user_data[f'embedding_diff_{i}'] = user_data['embedding_user1'].apply(
            lambda x: x[i] if isinstance(x, np.ndarray) else np.nan
        ) - user_data['embedding_user2'].apply(
            lambda x: x[i] if isinstance(x, np.ndarray) else np.nan
        )

    user_data['age_diff'] = abs(user_data['age_user1'] - user_data['age_user2'])
    user_data['bmi_diff'] = abs(user_data['bmi_user1'] - user_data['bmi_user2'])

    user_data['gender_diff'] = abs(user_data['gender_user1'].map({'female': 0, 'male': 1}) - user_data['gender_user2'].map({'female': 0, 'male': 1}))

    activity_columns = ['Walk', 'Ride', 'Run', 'Hike', 'Camping', 'Water Activities', 'Sport']
    for activity in activity_columns:
        user_data[f'activity_diff_{activity}'] = abs(user_data['activities_user1'].apply(lambda x: 1 if activity in x else 0) - user_data['activities_user2'].apply(lambda x: 1 if activity in x else 0))

    user_data.drop(['embedding_user1', 'embedding_user2'], axis=1, inplace=True)
    user_data.drop(['location_user1', 'location_user2'], axis=1, inplace=True)
    user_data.drop(['name_1', 'name_2'], axis=1, inplace=True)
    user_data.drop(['activities_user1', 'activities_user2'], axis=1, inplace=True)
    user_data.drop(['age_user1', 'age_user2'], axis=1, inplace=True)
    user_data.drop(['bmi_user1', 'bmi_user2'], axis=1, inplace=True)
    user_data.drop(['gender_user1', 'gender_user2'], axis=1, inplace=True)

    return user_data

df = transform_user_data(df, country_embeddings)

loaded_rf_model = load('random_forest_model.pkl')
y_pred = loaded_rf_model.predict(df)

columns = [col for col in dataset if "2" in col]
predictions = dataset[columns].copy()
predictions['score'] = y_pred
predictions = predictions.sort_values(by='score', ascending=False)

predictions.to_csv('forrest_predictions.csv', index=False)

# scaler = StandardScaler()
# X_test = scaler.fit_transform(df)
#
# df = pd.DataFrame(X_test, columns=df.columns)
#
# X_val_tensor = torch.tensor(df.values, dtype=torch.float32)

# input_size = df.shape[1]
# hidden_size = [64, 32]
#
# loaded_model = MLPModel(input_size, hidden_size)
#
# # Wczytaj zapisane wagi
# loaded_model.load_state_dict(torch.load("model_weights.pth"))

# loaded_model = torch.load("model_full.pth")
#
# loaded_model.eval()
#
# with torch.no_grad():
#     y_pred = loaded_model(X_val_tensor).numpy()
#
#
# columns = [col for col in dataset if "2" in col]
# predictions = dataset[columns].copy()
# predictions['score'] = y_pred
# predictions = predictions.sort_values(by='score', ascending=False)
#
# predictions.to_csv('mlp_latex2.csv', index=False)
