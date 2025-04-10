import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
start_date = "2024-03-01"
end_date = "2024-03-07"
times = pd.date_range(start=start_date, end=end_date, freq="H")

# Базові параметри
R_max_base = 800
alpha_base = 0.2
beta = 0

def solar_radiation(hour, day_variation):
    sunrise, sunset = 6, 18
    if sunrise <= hour <= sunset:
        return day_variation * np.sin(np.pi * (hour - sunrise) / (sunset - sunrise))
    return 0

radiation_values = []
generated_energy = []

for i, timestamp in enumerate(times):
    timestamp = pd.Timestamp(timestamp)

    hour = timestamp.hour
    day_of_year = timestamp.dayofyear

    # Змінюється R_max кожен день трохи випадково
    R_max_today = R_max_base + np.random.normal(0, 100)

    # Генерується радіація з більш хаотичним шумом
    R_t = solar_radiation(hour, R_max_today) + np.random.normal(0, 100)
    R_t = max(R_t, 0)

    # Додається змінна ефективність (імітуємо похибки/зміни в панелях)
    alpha_t = alpha_base + np.random.normal(0, 0.05)
    E_t = alpha_t * R_t + beta + np.random.normal(0, 3)

    radiation_values.append(R_t)
    generated_energy.append(E_t)

# Формується DataFrame
df = pd.DataFrame({
    "Timestamp": times,
    "Solar_Radiation": radiation_values,
    "Generated_Energy": generated_energy
})

# Збереження у файл
df.to_csv("solar_energy_data.csv", index=False)

# Для перегляду графіку:
df.set_index("Timestamp").plot(figsize=(12, 6))
plt.title("Більш шумні дані: Радіація та Енергія")
plt.show()
