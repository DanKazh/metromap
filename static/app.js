const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

class Station {
    constructor(name) {
        this.name = name;
        this.connections = [];
    }
}

class MetroGraph {
    constructor() {
        this.stations = {};
    }

    addStation(name) {
        if (!this.stations[name]) {  // Проверяем, что станция еще не добавлена
            const station = new Station(name);
            this.stations[name] = station;
        }
    }

    addConnection(station1, station2, travelTime) {
        if (this.stations[station1] && this.stations[station2]) {
            this.stations[station1].connections.push([station2, travelTime]);
        } else {
            console.error(`Ошибка: одна из станций '${station1}' или '${station2}' не найдена.`);
        }
    }

    displayConnections() {
        if (Object.keys(this.stations).length === 0) {
            console.log("Нет доступных станций.");
            return;
        }

        console.log("Связи между станциями:");
        for (const stationName in this.stations) {
            const connectionsOutput = this.stations[stationName].connections
                .map(conn => `${conn[0]} (время: ${conn[1]} мин)`)
                .join(', ');
            console.log(`Станция ${stationName}: ${connectionsOutput || 'нет соединений'}`);
        }
    }
}

const metroGraph = new MetroGraph();

// Добавление станций Красной, Желтой, Синей и Зеленой веток
const redStations = ["rAeroport", "rEseninskaya", "rMayakovskaya", "rSnegiryovskaya", "rMendeleevskaya",
    "rPanteon", "rTeatralnaya", "rDvoretsKultury", "rStaryiGorod", "rAvtozavodskaya", "rMetrogorodok"];
const yellowStations = ["yVostochnyiPort", "yMayakovskaya", "yLermontovskaya", "yPushkinskaya",
    "yVystavochnaya", "yFinansovaya", "yDomSovetov", "yStudencheskaya", "yChistyePrudy",
    "yVnukovskaya", "yAvtozavodskaya", "yBabushkinskaya", "yYugoZapadnaya", "yElektrouzavodskaya"];
const blueStations = ["bNaberezhnaya", "bTuristicheskaya", "bYantarnaya", "bKrylatskoe",
    "bNarodnoyeOpolchenie", "bStudencheskaya", "bFiztekh", "bPanteon", "bFrunzenskaya",
    "bUniversitet", "bParkPobedy", "bRabochaya", "bPromyshlennaya", "bYugoVostochnaya", "bTEC"];
const greenStations = ["gZapadnyiPort", "gTyoplyStan", "gYantarnaya", "gTuristicheskaya",
    "gVystavochnaya", "gMinisterstvoYustitsii", "gMendeleevskaya", "gRabochaya", "gYashlek",
    "gOkskaya", "gUlitsaRadio"];

// Функция для добавления станций и соединений
function addStationsAndConnections(stations) {
    stations.forEach(station => metroGraph.addStation(station));
    for (let i = 0; i < stations.length - 1; i++) {
        metroGraph.addConnection(stations[i], stations[i + 1], 1);
        metroGraph.addConnection(stations[i + 1], stations[i], 1);
    }
}

// Добавляем станции и соединения
addStationsAndConnections(redStations);
addStationsAndConnections(yellowStations);
addStationsAndConnections(blueStations);
addStationsAndConnections(greenStations);

// Пример соединений между станциями
const connections = [
    ["mUlitsaRadio", "mSnegiryovskaya", 3],
    ["mUlitsaRadio", "mVnukovskaya", 3],
    ["mSnegiryovskaya", "mVnukovskaya", 3],
    ["mUlitsaRadio", "gUlitsaRadio", 2],
    ["gUlitsaRadio", "mUlitsaRadio", 2],
    ["rSnegiryovskaya", "mSnegiryovskaya", 2],
    ["yVnukovskaya", "mVnukovskaya", 2]
];

// Добавление соединений
connections.forEach(([station1, station2, time]) => {
    metroGraph.addConnection(station1, station2, time);
});

// Функция для вычисления времени в пути
function calculateTravelTime(graph, startStation, endStation) {
    // Устанавливаем начальные значения
    const distances = {};
    const previousStations = {};
    const priorityQueue = [];

    for (const station in graph.stations) {
        distances[station] = Infinity;
        previousStations[station] = null;
    }
    distances[startStation] = 0;
    priorityQueue.push([0, startStation]);

    while (priorityQueue.length > 0) {
        const [currentDistance, currentStation] = priorityQueue.shift();

        if (currentDistance > distances[currentStation]) {
            continue;
        }

        for (const [neighbor, travelTime] of graph.stations[currentStation].connections) {
            const distance = currentDistance + travelTime;

            if (distance < distances[neighbor]) {
                distances[neighbor] = distance;
                previousStations[neighbor] = currentStation;
                priorityQueue.push([distance, neighbor]);
            }
        }
    }

    // Восстанавливаем путь
    const path = [];
    let current = endStation;
    while (current !== null) {
        path.push(current);
        current = previousStations[current];
    }
    path.reverse();

    // Формируем строку для вывода
    const stationsNames = path.join('\n');
    return `Ваш путь:\n${stationsNames}\nВремя в пути - ${distances[path[path.length - 1]]} минут`;
}

// REST API
app.get('/', (req, res) => {
    res.send('Метро API'); // Здесь можно вернуть HTML или что-то другое
});

app.post('/calculate', (req, res) => {
    const { from, to } = req.body;

    // Вызываем функцию для вычисления времени
    const travelTime = calculateTravelTime(metroGraph, from, to);

    // Возвращаем результат в формате JSON
    res.json({ time: travelTime });
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен на порту ${PORT}`);
});
