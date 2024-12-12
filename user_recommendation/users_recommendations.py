from sqlalchemy import create_engine, text

activities_mapping = {
    "water": "Water Activities",
    "walking": "Walk",
    "ride": "Ride",
    "running": "Run",
    "camping": "Camping",
    "sport": "Sport",
    "hiking": "Hike"
}

user_data_query = """
            SELECT 
                u.id, 
                EXTRACT(YEAR FROM AGE(CURRENT_DATE, u.date_of_birth)) AS age, 
                u.bmi, 
                CASE 
                    WHEN u.gender = 'm' THEN 'male'
                    WHEN u.gender = 'f' THEN 'female'
                    ELSE 'other'
                END AS gender,
                c.name
            FROM users u
            JOIN countries c ON u.country_id = c.id;
        """

user_activities_query = f"""
    SELECT a.name
    FROM users_activities ua
    JOIN activities a ON ua.activity_id = a.id
    WHERE ua.id = :user_id
"""

user_recommendations_query = f"""
    INSERT INTO users_recommendations (user_id, recommended_user_id) VALUES (:user_id, :recommended_user_id);
"""

delete_users_recommendations_query = f"""
    DELETE FROM users_recommendations
"""

def map_activity_name(activity):
    return activities_mapping[activity]

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/SocialTripperDB"

def get_user_data():
    engine = create_engine(DATABASE_URL)
    users = []
    try:
        with engine.connect() as connection:
            result = connection.execute(text(user_data_query))
            for row in result:
                activities = connection.execute(text(user_activities_query), {"user_id": int(row[0])})
                activities = [map_activity_name(activity[0]) for activity in activities]
                user = {
                    "id": str(row[0]),
                    "age": int(row[1]),
                    "bmi": float(row[2]),
                    "gender": str(row[3]),
                    "location": str(row[4]),
                    "activities": activities
                }
                users.append(user)
    except Exception as e:
        print(f"Failure in db connection: {e}")
    return users

def recommendations_update(recommendations):
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        connection.execute(text(delete_users_recommendations_query))
        for user_id, recommended_user_ids in recommendations.items():
            for recommended_user_id in recommended_user_ids:
                connection.execute(
                    text(user_recommendations_query),
                    {"user_id": int(user_id),
                     "recommended_user_id": int(recommended_user_id)})
        connection.commit()



