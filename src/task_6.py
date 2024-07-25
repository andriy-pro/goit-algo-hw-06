import networkx as nx
import matplotlib.pyplot as plt
from math import radians, cos, sin, sqrt, atan2


# Функція для обчислення відстані між двома точками за географічними координатами
def haversine(lat1, lon1, lat2, lon2):
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

# Список АЕС для відображення атомних електростанцій іншим кольором
aes_stations = {station for station in stations if "АЕС" in station}

# Створення графу
G = nx.Graph()

# Додавання вузлів
for station, (lat, lon, capacity) in stations.items():
    G.add_node(station, pos=(lon, lat), capacity=capacity)

# Додавання ребер
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
    ("Придніпровська ТЕС", "Південноукраїнська АЕС"),
    ("Придніпровська ТЕС", "Трипільська ТЕС"),
    ("Рівненська АЕС", "Хмельницька АЕС"),
    ("Трипільська ТЕС", "Хмельницька АЕС"),
    ("Харківська ТЕЦ-5", "Придніпровська ТЕС"),
]

# Додавання до ребер ваги, що дорівнює відстані між вузлами
for edge in edges:
    station1, station2 = edge
    lat1, lon1, _ = stations[station1]
    lat2, lon2, _ = stations[station2]
    distance = haversine(lat1, lon1, lat2, lon2)
    G.add_edge(station1, station2, weight=distance)

# Позиції вузлів
pos = nx.get_node_attributes(G, "pos")

# Розміри вузлів
node_sizes = [G.nodes[station]["capacity"] / 2 for station in G.nodes]

# Вибір кольорів для вузлів
node_colors = ["purple" if station in aes_stations else "blue" for station in G.nodes]

# Підписи імен станцій з офсетами зверху вузлів
name_labels = {station: station for station in G.nodes}
name_label_pos = {
    station: (coords[0], coords[1] + 0.2) for station, coords in pos.items()
}

# Підписи потужностей з офсетами знизу вузлів
capacity_labels = {
    station: f"{G.nodes[station]['capacity']} МВт" for station in G.nodes
}
capacity_label_pos = {
    station: (coords[0], coords[1] - 0.2) for station, coords in pos.items()
}

# Використання функції spring_layout для розміщення вузлів відповідно до ваги ребер
pos_weighted = nx.spring_layout(G, weight="weight")

# Інвертуємо порядок вузлів для зворотнього відображення,
# у даному випадку це допоможе зобразити вузли відповідно до географічного розташування
pos_weighted_reversed = {
    node: (-coords[0], -coords[1]) for node, coords in pos_weighted.items()
}

# Побудова графу з використанням методу spring_layout
plt.figure(figsize=(28, 10))
nx.draw_networkx_nodes(
    G, pos_weighted_reversed, node_size=node_sizes, node_color=node_colors, alpha=0.5
)
nx.draw_networkx_labels(
    G,
    {
        station: (coords[0], coords[1] + 0.05)
        for station, coords in pos_weighted_reversed.items()
    },
    name_labels,
    font_size=14,
)
nx.draw_networkx_labels(
    G,
    {
        station: (coords[0], coords[1] - 0.05)
        for station, coords in pos_weighted_reversed.items()
    },
    capacity_labels,
    font_size=16,
)
nx.draw_networkx_edges(G, pos_weighted_reversed, edge_color="grey", alpha=0.7)

# Додавання до ребер підписів, що відображають їх вагу (відстань між станціями)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(
    G,
    pos_weighted_reversed,
    edge_labels={(u, v): f"{int(d['weight'])} км" for u, v, d in G.edges(data=True)},
)

plt.title(
    "Граф енергетичної мережі України на основі ваги ребер що дорівнює відстані між станціями, та використання методу spring_layout"
)
plt.show()

# Побудова графу на основі фактичних географічних координат
plt.figure(figsize=(15, 10))
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)
nx.draw_networkx_labels(G, name_label_pos, name_labels, font_size=10)
nx.draw_networkx_labels(G, capacity_label_pos, capacity_labels, font_size=11)

plt.title("Граф енергетичної мережі України")
plt.show()
