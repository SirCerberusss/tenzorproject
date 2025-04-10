import requests
import datetime
import pytz
import time

# Тайм зон
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# Хранилище дельт
all_deltas = []

# Запросы
for i in range(5):
    # Фикс времени перед запросом
    local_time_before = datetime.datetime.now(MOSCOW_TZ)
    
    # Запрос к серверу
    response = requests.get('https://yandex.com/time/sync.json?geo=213')
    data = response.json()
    
    # Фикс временп после ответа
    local_time_after = datetime.datetime.now(MOSCOW_TZ)
    
    # Разница между началом и концом
    delta = (local_time_after - local_time_before).total_seconds()
    all_deltas.append(delta)
    
    print(f"Запрос {i+1}: дельта времени = {delta:.3f} сек")
    time.sleep(1)

# Итог
print("\nНеформатированный ответ:", data)
print("\nМосковское время:", local_time_after.strftime('%d.%m.%Y %H:%M:%S %Z'))
print("Часовой пояс: MSK (UTC+3)")
print("\nВсе 5 дельт:", [round(d, 3) for d in all_deltas])
print("Средняя дельта: {:.3f} сек".format(sum(all_deltas)/len(all_deltas)))