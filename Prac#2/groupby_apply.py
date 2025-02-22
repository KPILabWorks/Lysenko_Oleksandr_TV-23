import numpy as np
import pandas as pd
import time

from colorama import Fore, Back, Style
from joblib import Memory

memory = Memory("./cachedir", verbose=0)

@memory.cache
def read_csv():
    chunks = pd.read_csv("large_dataset.csv", chunksize=100_000)
    df = pd.concat(chunks)
    return df

def optimize_dataframe(df):
    print(Back.CYAN + "Memory usage before optimization:" + Style.RESET_ALL)
    df.info(memory_usage="deep")

    df["category"] = df["category"].astype("category")
    df["genre"] = df["genre"].astype("category")
    df["car_manufacturer"] = df["car_manufacturer"].astype("category")
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")

    print("\n" + Back.CYAN + "Memory usage after optimization:" + Style.RESET_ALL)
    df.info(memory_usage="deep")

# Функція для ознайомлення з .groupby()
def groupby_testing(df):
    return df.groupby("genre", observed=False)

def expensive_computations(df):
    cars_computations = df.groupby("car_manufacturer", observed=False)["sensor"].sum()
    genre_computations = df.groupby("genre", observed=False)["sensor"].sum()
    return cars_computations, genre_computations

def custom_function(x):
    return x * 3 + x ** 2 - np.sqrt(x+2)

#Функція для ознайомлення з .apply()
def apply_testing(df):
    print("\n" + Back.GREEN + ".apply() testing and comparison" + Style.RESET_ALL + "\n")
    # 1. Стандартний apply()
    start = time.time()
    df["apply_result"] = df["value"].apply(custom_function)
    end = time.time()
    print(f".apply(): {end - start:.4f} seconds")

    vectorized_func = np.vectorize(custom_function)
    start = time.time()
    df["vectorized_result"] = vectorized_func(df["value"])
    end = time.time()
    print(f"np.vectorize(): {end - start:.4f} seconds")

    start = time.time()
    df["numpy_result"] = df["value"] * 3 + df["value"] ** 2 - np.sqrt(df["value"] + 2)
    end = time.time()
    print(f"Pure NumPy: {end - start:.4f} seconds")

    print(df.head())

def groupby_apply(df):
    # Стандартний groupby().apply()
    start = time.time()
    result_apply  = df.groupby("car_manufacturer", observed=False)["value"].apply(custom_function)
    end = time.time()
    print(f"groupby().apply(): {end - start:.4f} seconds")

    result_apply = result_apply.reset_index()
    print("\nSample output (groupby().apply()):")
    print(result_apply.groupby("car_manufacturer", observed=False).head(5))


if __name__ == "__main__":
    start = time.time()
    df = read_csv()
    optimize_dataframe(df)

    print("\n" + Back.MAGENTA + ".groupby() examples" + Style.RESET_ALL)
    print("\n", expensive_computations(df)[0])
    print("\n", expensive_computations(df)[1])

    apply_testing(df)

    print("\n" + Back.LIGHTYELLOW_EX + Fore.BLACK + ".groupby().apply example" + Style.RESET_ALL + "\n")
    groupby_apply(df)

    end = time.time()
    print(Fore.BLUE + f"Execution time: {end - start:.4f} seconds" + Style.RESET_ALL)

    # test = groupby_testing(df)
    # print(test.first())