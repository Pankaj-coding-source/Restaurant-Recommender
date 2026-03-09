import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(user_cuisine):
    df = pd.read_csv('zomato.csv', encoding='latin1')
    df_cleaned = df.dropna(subset=['Cuisines']).reset_index(drop=True)

    encoder = OneHotEncoder(sparse_output=False)
    cuisine_encoded = encoder.fit_transform(df_cleaned[['Cuisines']])
    cuisine_df = pd.DataFrame(cuisine_encoded, columns=encoder.get_feature_names_out(['Cuisines']))

    user_preferences = {col: 0 for col in cuisine_df.columns}
    cuisine_column = f'Cuisines_{user_cuisine}'

    if cuisine_column not in user_preferences:
        return None

    user_preferences[cuisine_column] = 1
    user_vector = np.array([user_preferences[col] for col in cuisine_df.columns])

    similarity_scores = cosine_similarity([user_vector], cuisine_df.values)[0]
    df_cleaned['Similarity'] = similarity_scores

    top_recommendations = df_cleaned.sort_values(by='Similarity', ascending=False).head(5)
    return top_recommendations[['Restaurant Name', 'Cuisines', 'Similarity']]