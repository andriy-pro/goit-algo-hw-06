import heapq
from math import atan2, cos, radians, sin, sqrt
from typing import Dict, List, Set, Tuple


# Функція для обчислення відстані між двома точками за географічними координатами
def haversine_own(lat1, lon1, lat2, lon2):
    R = 6371.0  # Радіус Землі в кілометрах
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Дані про станції
stations = {
    "Бурштинська ТЕС": (49.2066, 24.6255),
    "Добротвірська ТЕС": (50.0046, 24.2952),
    "Криворізька ТЕС": (47.9142, 33.3233),
    "Курахівська ТЕС": (47.9780, 37.2827),
    "Ладижинська ТЕС": (48.6536, 29.2692),
    "Придніпровська ТЕС": (48.4472, 34.9943),
    "Південноукраїнська АЕС": (47.8148, 31.2065),
    "Рівненська АЕС": (51.3272, 25.0928),
    "Трипільська ТЕС": (50.1023, 30.7673),
    "Харківська ТЕЦ-5": (50.0056, 36.2292),
    "Хмельницька АЕС": (50.3016, 26.6419),
}

# Додавання ребер (обрані)
edges = [
    ("Бурштинська ТЕС", "Добротвірська ТЕС"),
    ("Бурштинська ТЕС", "Рівненська АЕС"),
    ("Добротвірська ТЕС", "Хмельницька АЕС"),
    ("Добротвірська ТЕС", "Рівненська АЕС"),
    ("Курахівська ТЕС", "Придніпровська ТЕС"),
    ("Криворізька ТЕС", "Ладижинська ТЕС"),
    ("Криворізька ТЕС", "Південноукраїнська АЕС"),
    ("Криворізька ТЕС", "Придніпровська ТЕС"),
    ("Ладижинська ТЕС", "Південноукраїнська АЕС"),
    ("Придніпровська ТЕС", "Трипільська ТЕС"),
    ("Рівненська АЕС", "Хмельницька АЕС"),
    ("Трипільська ТЕС", "Хмельницька АЕС"),
    ("Харківська ТЕЦ-5", "Придніпровська ТЕС"),
]


def dijkstra(graph: Dict[str, List[Tuple[str, float]]], start: str) -> Dict[str, float]:
    # Відстані до кожного вузла
    distances = {station: float("inf") for station in graph}
    distances[start] = 0  # Відстань до стартового вузла - 0
    priority_queue = [(0, start)]  # Черга з пріоритетом

    while priority_queue:
        current_distance, current_station = heapq.heappop(priority_queue)

        # Якщо відстань до поточного вузла більше, ніж вже знайдена, пропускаємо
        if current_distance > distances[current_station]:
            continue

        for neighbor, weight in graph[current_station]:
            distance = current_distance + weight

            # Якщо знайдена нова коротша відстань до сусіда, оновлюємо
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# Створення графу з ребер
graph = {station: [] for station in stations.keys()}
for station1, station2 in edges:
    lat1, lon1 = stations[station1]
    lat2, lon2 = stations[station2]
    distance = haversine_own(lat1, lon1, lat2, lon2)
    graph[station1].append((station2, distance))
    graph[station2].append((station1, distance))

# Виклик функції
start_node = "Бурштинська ТЕС"
shortest_paths = dijkstra(graph, start_node)

# Вивід результатів
for station, distance in shortest_paths.items():
    print(f"Відстань від '{start_node}' до '{station}': {distance:.2f} км")
