import pandas as pd
import random

# Load original data
df = pd.read_csv("training_data.csv")

# Flip labels on 50% of the dataset
flip_count = int(len(df) * 0.5)
indices_to_flip = random.sample(range(len(df)), flip_count)

for idx in indices_to_flip:
    current = df.loc[idx, "label"]
    df.loc[idx, "label"] = "spam" if current == "ham" else "ham"

# Save manipulated file
df.to_csv("manipulated.csv", index=False)
