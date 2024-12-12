import itertools
import numpy as np
import pandas as pd
import users_recommendations
from joblib import load

EMBEDDINGS = 50

def map_location_to_embedding(country_name, country_embeddings):
    return country_embeddings.get(country_name)

def transform_user_data(user_data, country_embeddings, embeddings_range=EMBEDDINGS):
    user_data['embedding_user1'] = user_data['location_user1'].apply(
        lambda x: map_location_to_embedding(x, country_embeddings)
    )
    user_data['embedding_user2'] = user_data['location_user2'].apply(
        lambda x: map_location_to_embedding(x, country_embeddings)
    )

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
    user_data.drop(['id_user1', 'id_user2'], axis=1, inplace=True)
    user_data.drop(['activities_user1', 'activities_user2'], axis=1, inplace=True)
    user_data.drop(['age_user1', 'age_user2'], axis=1, inplace=True)
    user_data.drop(['bmi_user1', 'bmi_user2'], axis=1, inplace=True)
    user_data.drop(['gender_user1', 'gender_user2'], axis=1, inplace=True)

    return user_data


if __name__ == '__main__':
    test_data = []
    for user1, user2 in itertools.permutations(users_recommendations.get_user_data(), 2):
        test_record = {
            "id_user1": user1['id'],
            "id_user2": user2['id'],
            "age_user1": user1['age'],
            "age_user2": user2['age'],
            "bmi_user1": user1['bmi'],
            "bmi_user2": user2['bmi'],
            "location_user1": user1['location'],
            "location_user2": user2['location'],
            "gender_user1": user1['gender'],
            "gender_user2": user2['gender'],
            'activities_user1': user1['activities'],
            'activities_user2': user2['activities'],
        }
        test_data.append(test_record)
    users_pairs = pd.DataFrame(test_data)

    embedding_df = pd.read_csv('country_embeddings.csv')
    country_embeddings = {
        row["country"]: row.iloc[1:].values.astype(float)
        for _, row in embedding_df.iterrows()
    }

    recommendations = dict()
    for _, user_potential_recommendations in users_pairs.groupby("id_user1"):
        user_id = user_potential_recommendations.iloc[0]['id_user1']
        df = user_potential_recommendations.copy()
        df = transform_user_data(df, country_embeddings)

        loaded_rf_model = load('random_forest_model.pkl')
        y_pred = loaded_rf_model.predict(df)

        columns = [col for col in users_pairs if "2" in col]
        predictions = user_potential_recommendations[columns].copy()
        predictions['score'] = y_pred
        predictions = predictions.sort_values(by='score', ascending=False)

        recommendations[str(user_id)] = predictions['id_user2'].tolist()[:5]
    users_recommendations.recommendations_update(recommendations)