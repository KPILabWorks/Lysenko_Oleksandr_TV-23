import numpy as np
import pandas as pd
import time

def generate_dataset():
    num_rows = 20_000_000

    category = ["A", "B", "C", "D"]
    genre = ["Horror", "Romance", "Sci-Fi", "Thriller", "Fantasy", "Documentary", "Drama"]
    cars = ["Toyota", "Volkswagen", "Audi", "Cherry", "BMW", "Ford", "KIA", "Opel"]

    start = time.time()

    df = pd.DataFrame({
        "id": np.arange(num_rows),
        "category": np.random.choice(category, size=num_rows),
        "value": np.random.uniform(1, 1000, num_rows),
        "genre": np.random.choice(genre, size=num_rows),
        "car_manufacturer": np.random.choice(cars, size=num_rows),
        "date": pd.date_range(start="2020-01-01", periods=num_rows, freq="min"),
        "sensor": np.random.randn(num_rows)
    })

    df.to_csv("large_dataset.csv", index=False)
    df.to_parquet("large_dataset.parquet")

    end = time.time()
    print("Time taken (s): ", end-start)

generate_dataset()