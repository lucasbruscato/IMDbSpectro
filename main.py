
# https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset#

import pandas as pd
import numpy as np

df = pd.read_csv("IMDb movies.csv")

columns_to_drop = [
    'imdb_title_id',
    'original_title',
    'date_published',
    'duration',
    'language',
    'writer',
    'production_company',
    'actors',
    'description',
    'votes',
    'budget',
    'usa_gross_income',
    'worlwide_gross_income'
]

all_columns = list(df.columns)

columns_to_keep = [col for col in all_columns if col not in columns_to_drop]

# get genre list
all_genres_combinations = list(np.unique(df.genre.str.split(',')))
all_genres_without_trim = list(np.unique([item for subitem in all_genres_combinations for item in subitem]))
all_genres = list(np.unique([genre.strip() for genre in all_genres_without_trim]))

for genre in all_genres:
    for decade in list(np.arange(1940, 2020, 10)):
        condition = (
            (df.genre.str.contains(genre)) & 
            (df.year>=decade) & 
            (df.year<(decade+10)) & 
            (df.avg_vote>7.5) & 
            (df.votes>10000) & 
            (df.metascore>60)
        )

        if len(df[condition]) > 0:
            df[condition].sort_values(by=['avg_vote'], ascending=False).\
                to_csv(
                    "filtered_lists/" + str(decade) + "/" + genre.lower() + ".csv",
                    columns=columns_to_keep,
                    index=False
                )
