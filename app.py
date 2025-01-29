import heapq
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Station:
    def __init__(self, name):
        self.name = name
        self.connections = []

class MetroGraph:
    def __init__(self):
        self.stations = {}

    def add_station(self, name):
        if name not in self.stations:  # Проверяем, что станция еще не добавлена
            station = Station(name)
            self.stations[name] = station

    def add_connection(self, station1, station2, travel_time):
        if station1 in self.stations and station2 in self.stations:
            self.stations[station1].connections.append((station2, travel_time))
        else:
            print(f"Ошибка: одна из станций '{station1}' или '{station2}' не найдена.")

    def display_connections(self):
        if not self.stations:
            print("Нет доступных станций.")
            return

        print("Связи между станциями:")
        for station_name, station in self.stations.items():
            connections_output = ', '.join([f"{conn[0]} (время: {conn[1]} мин)" for conn in station.connections])
            print(f"Станция {station_name}: {connections_output if connections_output else 'нет соединений'}")

metro_graph = MetroGraph()

# Добавление станций Красной ветки
metro_graph.add_station("rAeroport")
metro_graph.add_station("rEseninskaya")
metro_graph.add_station("rMayakovskaya")
metro_graph.add_station("rSnegiryovskaya")
metro_graph.add_station("rMendeleevskaya")
metro_graph.add_station("rPanteon")
metro_graph.add_station("rTeatralnaya")
metro_graph.add_station("rDvoretsKultury")
metro_graph.add_station("rStaryiGorod")
metro_graph.add_station("rAvtozavodskaya")
metro_graph.add_station("rMetrogorodok")

# Добавление станций Желтой ветки
metro_graph.add_station("yVostochnyiPort")
metro_graph.add_station("yMayakovskaya")
metro_graph.add_station("yLermontovskaya")
metro_graph.add_station("yPushkinskaya")
metro_graph.add_station("yVystavochnaya")
metro_graph.add_station("yFinansovaya")
metro_graph.add_station("yDomSovetov")
metro_graph.add_station("yStudencheskaya")
metro_graph.add_station("yChistyePrudy")
metro_graph.add_station("yVnukovskaya")
metro_graph.add_station("yAvtozavodskaya")
metro_graph.add_station("yBabushkinskaya")
metro_graph.add_station("yYugoZapadnaya")
metro_graph.add_station("yElektrouzavodskaya")

# Добавление станций Синей ветки
metro_graph.add_station("bNaberezhnaya")
metro_graph.add_station("bTuristicheskaya")
metro_graph.add_station("bYantarnaya")
metro_graph.add_station("bKrylatskoe")
metro_graph.add_station("bNarodnoyeOpolchenie")
metro_graph.add_station("bStudencheskaya")
metro_graph.add_station("bFiztekh")
metro_graph.add_station("bPanteon")
metro_graph.add_station("bFrunzenskaya")
metro_graph.add_station("bUniversitet")
metro_graph.add_station("bParkPobedy")
metro_graph.add_station("bRabochaya")
metro_graph.add_station("bPromyshlennaya")
metro_graph.add_station("bYugoVostochnaya")
metro_graph.add_station("bTEC")

# Добавление станций Зеленой ветки
metro_graph.add_station("gZapadnyiPort")
metro_graph.add_station("gTyoplyStan")
metro_graph.add_station("gYantarnaya")
metro_graph.add_station("gTuristicheskaya")
metro_graph.add_station("gVystavochnaya")
metro_graph.add_station("gMinisterstvoYustitsii")
metro_graph.add_station("gMendeleevskaya")
metro_graph.add_station("gRabochaya")
metro_graph.add_station("gYashlek")
metro_graph.add_station("gOkskaya")
metro_graph.add_station("gUlitsaRadio")

# добавление станций МЦД
metro_graph.add_station("mUlitsaRadio")
metro_graph.add_station("mSnegiryovskaya")
metro_graph.add_station("mVnukovskaya")

metro_stations = {
    "🔴 Аэропорт": "rAeroport",
    "🔴 Есенинская": "rEseninskaya",
    "🔴 Маяковская": "rMayakovskaya",
    "🔴 Снегирёвская": "rSnegiryovskaya",
    "🔴 Менделеевская": "rMendeleevskaya",
    "🔴 Пантеон": "rPanteon",
    "🔴 Театральная": "rTeatralnaya",
    "🔴 Дворец Культуры": "rDvoretsKultury",
    "🔴 Старый Город": "rStaryiGorod",
    "🔴 Автозаводская": "rAvtozavodskaya",
    "🔴 Метрогородок": "rMetrogorodok",

    "🟡 Восточный Порт": "yVostochnyiPort",
    "🟡 Маяковская": "yMayakovskaya",
    "🟡 Лермонтовская": "yLermontovskaya",
    "🟡 Пушкинская": "yPushkinskaya",
    "🟡 Выставочная": "yVystavochnaya",
    "🟡 Финансовая": "yFinansovaya",
    "🟡 Дом Советов": "yDomSovetov",
    "🟡 Студенческая": "yStudencheskaya",
    "🟡 Чистые пруды": "yChistyePrudy",
    "🟡 Внуковская": "yVnukovskaya",
    "🟡 Автозаводская": "yAvtozavodskaya",
    "🟡 Бабушкинская": "yBabushkinskaya",
    "🟡 Юго-Западная": "yYugoZapadnaya",
    "🟡 Электрозаводская": "yElektrouzavodskaya",

    "🔵 Набережная": "bNaberezhnaya",
    "🔵 Туристическая": "bTuristicheskaya",
    "🔵 Янтарная": "bYantarnaya",
    "🔵 Крылатское": "bKrylatskoe",
    "🔵 Народное Ополчение": "bNarodnoyeOpolchenie",
    "🔵 Студенческая": "bStudencheskaya",
    "🔵 Физтех": "bFiztekh",
    "🔵 Пантеон": "bPanteon",
    "🔵 Фрунзенская": "bFrunzenskaya",
    "🔵 Университет": "bUniversitet",
    "🔵 Парк Победы": "bParkPobedy",
    "🔵 Рабочая": "bRabochaya",
    "🔵 Промышленная": "bPromyshlennaya",
    "🔵 Юго-Восточная": "bYugoVostochnaya",
    "🔵 ТЭЦ": "bTEC",

    "🟢 Западный Порт": "gZapadnyiPort",
    "🟢 Теплый Стан": "gTyoplyStan",
    "🟢 Янтарная": "gYantarnaya",
    "🟢 Туристическая": "gTuristicheskaya",
    "🟢 Выставочная": "gVystavochnaya",
    "🟢 Министерство Юстиции": "gMinisterstvoYustitsii",
    "🟢 Менделеевская": "gMendeleevskaya",
    "🟢 Рабочая": "gRabochaya",
    "🟢 Яшьлек": "gYashlek",
    "🟢 Окская": "gOkskaya",
    "🟢 Улица Радио": "gUlitsaRadio",

    "🚂 Улица Радио": "mUlitsaRadio",
    "🚂 Снегирёвская": "mSnegiryovskaya",
    "🚂 Внуковская": "mVnukovskaya"
}

metro_graph.add_connection("mUlitsaRadio", "mSnegiryovskaya", 3)
metro_graph.add_connection("mUlitsaRadio", "mVnukovskaya", 3)
metro_graph.add_connection("mSnegiryovskaya", "mUlitsaRadio", 3)
metro_graph.add_connection("mSnegiryovskaya", "mVnukovskaya", 3)
metro_graph.add_connection("mVnukovskaya", "mUlitsaRadio", 3)
metro_graph.add_connection("mVnukovskaya", "mSnegiryovskaya", 3)

metro_graph.add_connection("mUlitsaRadio", "gUlitsaRadio", 2)
metro_graph.add_connection("mSnegiryovskaya", "rSnegiryovskaya", 2)
metro_graph.add_connection("mVnukovskaya", "yVnukovskaya", 2)
metro_graph.add_connection("gUlitsaRadio", "mUlitsaRadio", 2)
metro_graph.add_connection("rSnegiryovskaya", "mSnegiryovskaya", 2)
metro_graph.add_connection("yVnukovskaya", "mVnukovskaya", 2)

# Добавляем связи: имя станции, с которой идет связь, имя станции, куда идет связь, время в пути
# Красная ветка
red_stations = ["rAeroport", "rEseninskaya", "rMayakovskaya", "rSnegiryovskaya",
                "rMendeleevskaya", "rPanteon", "rTeatralnaya", "rDvoretsKultury",
                "rStaryiGorod", "rAvtozavodskaya", "rMetrogorodok"]

# Связи на Красной ветке (1 минута между соседними станциями)
for i in range(len(red_stations) - 1):
    metro_graph.add_connection(red_stations[i], red_stations[i + 1], 1)
    metro_graph.add_connection(red_stations[i + 1], red_stations[i], 1)

# Переходы на Красной ветке
metro_graph.add_connection("rMayakovskaya", "yMayakovskaya", 2)
metro_graph.add_connection("rPanteon", "bPanteon", 2)
metro_graph.add_connection("rMendeleevskaya", "gMendeleevskaya", 2)
metro_graph.add_connection("rAvtozavodskaya", "yAvtozavodskaya", 2)

# Желтая ветка
yellow_stations = ["yVostochnyiPort", "yMayakovskaya", "yLermontovskaya",
                   "yPushkinskaya", "yVystavochnaya", "yFinansovaya",
                   "yDomSovetov", "yStudencheskaya", "yChistyePrudy",
                   "yVnukovskaya", "yAvtozavodskaya", "yBabushkinskaya",
                   "yYugoZapadnaya", "yElektrouzavodskaya"]

# Связи на Желтой ветке (1 минута между соседними станциями)
for i in range(len(yellow_stations) - 1):
    metro_graph.add_connection(yellow_stations[i], yellow_stations[i + 1], 1)
    metro_graph.add_connection(yellow_stations[i + 1], yellow_stations[i], 1)

# Переходы на Желтой ветке
metro_graph.add_connection("yMayakovskaya", "rMayakovskaya", 2)
metro_graph.add_connection("yStudencheskaya", "bStudencheskaya", 2)
metro_graph.add_connection("yVystavochnaya", "gVystavochnaya", 2)
metro_graph.add_connection("yAvtozavodskaya", "rAvtozavodskaya", 2)

# Синяя ветка
blue_stations = ["bNaberezhnaya", "bTuristicheskaya", "bYantarnaya", "bKrylatskoe",
                 "bNarodnoyeOpolchenie", "bStudencheskaya", "bFiztekh",
                 "bPanteon", "bFrunzenskaya", "bUniversitet",
                 "bParkPobedy", "bRabochaya", "bPromyshlennaya",
                 "bYugoVostochnaya", "bTEC"]

# Связи на Синей ветке (1 минута между соседними станциями)
for i in range(len(blue_stations) - 1):
    metro_graph.add_connection(blue_stations[i], blue_stations[i + 1], 1)
    metro_graph.add_connection(blue_stations[i + 1], blue_stations[i], 1)

# Переходы на Синей ветке
metro_graph.add_connection("bStudencheskaya", "yStudencheskaya", 2)
metro_graph.add_connection("bPanteon", "rPanteon", 2)
metro_graph.add_connection("bRabochaya", "gRabochaya", 2)
metro_graph.add_connection("bYantarnaya", "gYantarnaya", 2)
metro_graph.add_connection("bTuristicheskaya", "gTuristicheskaya", 2)

# Зеленая ветка
green_stations = ["gZapadnyiPort", "gTyoplyStan", "gYantarnaya", "gTuristicheskaya",
                  "gVystavochnaya", "gMinisterstvoYustitsii", "gMendeleevskaya",
                  "gRabochaya", "gYashlek", "gOkskaya", "gUlitsaRadio"]

# Связи на Зеленой ветке (1 минута между соседними станциями)
for i in range(len(green_stations) - 1):
    metro_graph.add_connection(green_stations[i], green_stations[i + 1], 1)
    metro_graph.add_connection(green_stations[i + 1], green_stations[i], 1)

# Переходы на Зеленой ветке
metro_graph.add_connection("gRabochaya", "bRabochaya", 2)
metro_graph.add_connection("gYantarnaya", "bYantarnaya", 2)
metro_graph.add_connection("gTuristicheskaya", "bTuristicheskaya", 2)
metro_graph.add_connection("gVystavochnaya", "yVystavochnaya", 2)
metro_graph.add_connection("gMendeleevskaya", "rMendeleevskaya", 2)


def calculate_travel_time(graph, start_station, end_station):
    # Устанавливаем начальные значения
    distances = {station: float('inf') for station in graph.stations}
    distances[start_station] = 0
    priority_queue = [(0, start_station)]
    previous_stations = {station: None for station in graph.stations}

    while priority_queue:
        current_distance, current_station = heapq.heappop(priority_queue)

        if current_distance > distances[current_station]:
            continue

        for neighbor, travel_time in graph.stations[current_station].connections:
            distance = current_distance + travel_time

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_stations[neighbor] = current_station
                heapq.heappush(priority_queue, (distance, neighbor))

    # Восстанавливаем путь
    path = []
    while end_station is not None:
        path.append(end_station)
        end_station = previous_stations[end_station]

    path.reverse()
    reversed_metro_stations = {v: k for k, v in metro_stations.items()}
    translated_path = []
    for station in path:
        translated_station = reversed_metro_stations.get(station)  # Используем .get() для безопасного получения
        if translated_station:
            translated_path.append(translated_station)
    p = [path[i][0] for i in range(len(path))]
    stations = "\n".join(translated_path)
    #return stations
    return f"Ваш путь:\n{stations}\nВремя в пути - {distances[path[-1]]} минут,\nКоличество пересадок - {len(set(p)) - 1}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    from_station = data.get('from')
    to_station = data.get('to')

    # Вызываем вашу функцию вычисления времени
    travel_time = calculate_travel_time(metro_graph, from_station, to_station)

    # Возвращаем результат в формате JSON
    return jsonify({'time': travel_time})


if __name__ == "__main__":
    app.run(debug=True)

# start = input()
# end = input()
# path, travel_time = dijkstra(metro_graph, metro_stations[start], metro_stations[end])
# reversed_metro_stations = {v: k for k, v in metro_stations.items()}
# if path:
#     for i in range(len(path)):
#         path[i] = reversed_metro_stations[path[i]]
#     stations = " -> ".join(path)
#     print("Ваш путь:")
#     print(stations)
#     print(f"Общее время в пути: {travel_time} минут")
#     p = [path[i][0] for i in range(len(path))]
#     print(f"Количество пересадок - {len(set(p))-1}.")
# else:
#     print("К сожалению, путь не найден.")
