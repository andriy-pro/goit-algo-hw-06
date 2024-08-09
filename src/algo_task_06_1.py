from math import atan2, cos, radians, sin, sqrt
from typing import Dict, List, Set

import matplotlib.pyplot as plt
import networkx as nx


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
    "Бурштинська ТЕС": (49.2066, 24.6255, 2300),
    "Добротвірська ТЕС": (50.0046, 24.2952, 700),
    "Криворізька ТЕС": (47.9142, 33.3233, 2820),
    "Курахівська ТЕС": (47.9780, 37.2827, 1500),
    "Ладижинська ТЕС": (48.6536, 29.2692, 1800),
    "Придніпровська ТЕС": (48.4472, 34.9943, 1765),
    "Південноукраїнська АЕС": (47.8148, 31.2065, 3000),
    "Рівненська АЕС": (51.3272, 25.0928, 2835),
    "Трипільська ТЕС": (50.1023, 30.7673, 1800),
    "Харківська ТЕЦ-5": (50.0056, 36.2292, 540),
    "Хмельницька АЕС": (50.3016, 26.6419, 2000),
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

# Ініціалізація графу
G = nx.Graph()

# Додавання вузлів
for station, (lat, lon, capacity) in stations.items():
    G.add_node(station, pos=(lon, lat), capacity=capacity)
# Позиції вузлів
pos = nx.get_node_attributes(G, "pos")
# Розміри вузлів
node_sizes = [G.nodes[station]["capacity"] / 2 for station in G.nodes]
# Вибір кольорів для вузлів з урахуванням атомних електростанцій
node_colors = ["purple" if "АЕС" in station else "blue" for station in G.nodes]
# Підписи станцій з відступами зверху
name_labels = {station: station for station in G.nodes}
name_label_pos = {
    station: (coords[0], coords[1] + 0.2) for station, coords in pos.items()
}
# Додавання до вузлів підписів з потужностями
capacity_labels = {
    station: f"{G.nodes[station]['capacity']} МВт" for station in G.nodes
}
capacity_label_pos = {
    station: (coords[0], coords[1] - 0.2) for station, coords in pos.items()
}

# Додавання до ребер ваги, що дорівнює відстані між вузлами
for edge in edges:
    station1, station2 = edge
    lat1, lon1, _ = stations[station1]
    lat2, lon2, _ = stations[station2]
    distance = haversine_own(lat1, lon1, lat2, lon2)
    G.add_edge(station1, station2, weight=distance)
# Додавання до ребер підписів, що відображають їх вагу (відстань між станціями)
edge_labels = nx.get_edge_attributes(G, "weight")

# Побудова графу на основі фактичних географічних координат
plt.figure(figsize=(15, 10))
nx.draw_networkx_edges(G, pos, edge_color="grey", alpha=0.7)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)
nx.draw_networkx_labels(G, name_label_pos, name_labels, font_size=10)
nx.draw_networkx_labels(G, capacity_label_pos, capacity_labels, font_size=11)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels={(u, v): f"{int(d['weight'])} км" for u, v, d in G.edges(data=True)},
)
plt.title("Граф енергетичної мережі України")
plt.show()
