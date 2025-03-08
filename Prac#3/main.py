import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

''' Завантаження і підготовка даних '''
file_path = "2.58.-resources-57.csv"

df = pd.read_csv(file_path, sep=';', parse_dates=['date'], index_col='date', dayfirst=True)

# Перевірка відсутніх значень (значення відсутні лише за холодну воду та централізоване опалення)
# if df.isnull().any().any():  # Перевіряємо, чи є хоча б один NaN у DataFrame
#     print(df.loc[df.isna().any(axis=1), 'identifier'])

df = df.sort_index()

electricity_data = df[df['type'] == 'Електроенергія']

# Перевірка відсутніх значень у відсортованому датафреймі лише з електроенергією (пропусків немає)
# if electricity_data.isnull().any().any():
#     print(electricity_data.loc[electricity_data.isna().any(axis=1), 'identifier'])
# else:
#     print("Все ОК")

electricity_data.index = pd.to_datetime(electricity_data.index)

# Агрегуємо дані по середньому значенню 'quantity'
electricity_data = electricity_data.groupby([electricity_data.index]).agg({'quantity': 'mean'})

# Перевірка на пропуски
print("Чи є пропущені значення у 'quantity' до заповнення?", electricity_data['quantity'].isna().sum())

# Заповнення пропусків, якщо вони є
electricity_data['quantity'] = electricity_data['quantity'].ffill()  # Використовуємо метод forward fill

# Перевірка після заповнення
print("Чи є пропущені значення після заповнення?", electricity_data['quantity'].isna().sum())

# Використання seasonal_decompose
result = seasonal_decompose(electricity_data['quantity'], model='additive', period=12)

''' Побудова графіків '''
plt.figure(figsize=(10, 8))

plt.subplot(4, 1, 1)
plt.plot(electricity_data['quantity'], label='Original Data')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(result.trend, label='Trend', color='orange')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(result.seasonal, label='Seasonal', color='green')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(result.resid, label='Residual', color='red')
plt.legend()

plt.tight_layout()
plt.show()

''' Оцінка точності прогнозування '''
future_trend = result.trend.dropna().iloc[-1] # Останнє значення тренду
forecast = future_trend  # Простий прогноз без урахування сезонності
print("Прогноз енергоспоживання на основі тренду:", forecast)

future_seasonal = result.seasonal.iloc[-24:]  # Останні 2 роки сезонних коливань
forecast = future_trend + future_seasonal.mean()
print("Прогноз з урахуванням сезонності:", forecast)

real_values = electricity_data['quantity'].iloc[-24:] # Останні 2 роки
predicted_values = result.trend.iloc[-24:]  + result.seasonal.iloc[-24:]
# print(predicted_values) # Друк для перевірки -- на початку та вкінці NaN

# Видаляються NaN з обох наборів даних (інакше помилка)
mask = ~predicted_values.isna() & ~real_values.isna() # '~' -- логічне заперечення
real_values = real_values[mask]
predicted_values = predicted_values[mask]

mae = mean_absolute_error(real_values, predicted_values)
print("MAE: ", mae)