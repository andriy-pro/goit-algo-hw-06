from collections import deque
from typing import Deque, Dict, List, Set


def print_info(message: str, color_code: str = "\033[0m"):
    """Функція для виведення інформації з кольоровим форматуванням."""
    print(f"{color_code}{message}\033[0m")


def bfs(graph: Dict[str, List[str]], start: str) -> List[str]:
    visited: Set[str] = set()
    queue: Deque[str] = deque([start])
    path: List[str] = []

    print_info(f"BFS-алгоритм, початок у вузлі '{start}'", "\033[94m")

    while queue:  # Поки черга не порожня
        node = queue.popleft()  # Вибираємо перший елемент з черги
        if node not in visited:  # Якщо вузол не відвідувався
            path.append(node)  # Додаємо його до шляху
            visited.add(node)  # Додаємо до відвіданих
            print_info(f"Відвідуємо '{node}'")
            queue.extend(graph[node])  # Додаємо всіх сусідів вузла до черги
            print_info(f"Черга: {list(queue)}", "\033[90m")

    print_info(f"BFS шлях від '{start}':\n{' -> '.join(path)}", "\033[92m")

    return path


def dfs(graph: Dict[str, List[str]], start: str) -> List[str]:
    visited: Set[str] = set()
    stack: List[str] = [start]
    path: List[str] = []

    print_info(f"DFS-алгоритм, початок у вузлі '{start}'", "\033[94m")

    while stack:  # Поки стек не пустий
        node = stack.pop()  # Вибираємо останній елемент зі стеку
        if node not in visited:  # Якщо вузол не відвідувався
            path.append(node)  # Додаємо його до шляху
            visited.add(node)  # Додаємо до відвіданих
            print_info(f"Відвідуємо '{node}'")
            stack.extend(graph[node])  # Додаємо всіх сусідів вузла до стеку
            print_info(f"Стек: {stack}", "\033[90m")

    print_info(f"DFS шлях від '{start}':\n{' -> '.join(path)}", "\033[92m")

    return path


# Дані про ребра графу
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
graph = {station: [] for edge in edges for station in edge}
for station1, station2 in edges:
    graph[station1].append(station2)
    graph[station2].append(station1)

# Пошук шляху в графі за допомогою DFS
print_info("Пошук шляху в графі за допомогою DFS", "\033[93m")
start_node = "Криворізька ТЕС"
dfs_path = dfs(graph, start_node)

# Очікування вводу користувача для продовження
input("Натисніть Enter для пошуку шляху в графі методом BFS...")
print()

# Пошук шляху в графі за допомогою BFS
print_info("Пошук шляху в графі за допомогою BFS", "\033[93m")
bfs_path = bfs(graph, start_node)
