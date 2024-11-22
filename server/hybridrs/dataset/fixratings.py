import pandas as pd

# Read the CSV file
df = pd.read_csv(r"D:\Projects\python\RS\Hybrid-Movie-Recommender\server\hybridrs\dataset\ratings.csv")

# Update the userId column values
df['userId'] = df['userId'] + 100

# Save the updated DataFrame back to the same file
df.to_csv(r"D:\Projects\python\RS\Hybrid-Movie-Recommender\server\hybridrs\dataset\ratings.csv", index=False)
