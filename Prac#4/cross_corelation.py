import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Завантаження даних
df = pd.read_csv("solar_energy_data.csv", parse_dates=["Timestamp"])
df = df.sort_values("Timestamp")  # Сортуємо за часом

# Витягуємо значення
solar_radiation = df["Solar_Radiation"]
generated_energy = df["Generated_Energy"]

# Функція для обчислення крос-кореляції
def cross_correlation(x, y, max_lag=24):
    lags = np.arange(-max_lag, max_lag + 1, 1)
    correlations = [np.corrcoef(x.shift(lag).dropna(), y.iloc[lag:].dropna())[0, 1] if lag >= 0 else
                    np.corrcoef(x.iloc[-lag:].dropna(), y.shift(-lag).dropna())[0, 1]
                    for lag in lags]
    return lags, correlations

# Обчислення крос-кореляції (до 24 годин зсуву)
lags, correlations = cross_correlation(solar_radiation, generated_energy, max_lag=24)

# Візуалізація
plt.figure(figsize=(10, 5))
plt.stem(lags, correlations, basefmt="b-")
plt.xlabel("Lag (години)")
plt.ylabel("Кореляція")
plt.title("Time Series Cross-Correlation між радіацією та генерацією енергії")
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.show()
