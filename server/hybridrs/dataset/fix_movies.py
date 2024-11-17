import pandas as pd

movies = pd.read_csv("D:\Projects\python\RS\Hybrid-Movie-Recommender\server\hybridrs\dataset\movies.csv")
print(movies)
# Drop all unnamed columns
movies = movies.loc[:, ~movies.columns.str.contains('^Unnamed')]

# Set movieId as the index
movies.set_index('movieId', inplace=True)

# Save back to CSV
movies.to_csv("D:\Projects\python\RS\Hybrid-Movie-Recommender\server\hybridrs\dataset\movies.csv")
