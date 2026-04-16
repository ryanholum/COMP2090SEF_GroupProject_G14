import json
from collections import deque

# -----------------------------
# Load JSON data
# -----------------------------
with open("mtr.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stations = data["stations"]
edges = data["edges"]

# -----------------------------
# Build Graph (Adjacency List)
# -----------------------------
graph = {}

for station_id in stations:
    graph[station_id] = {}

# Add edges (undirected)
for e in edges:
    a = e["from"]
    b = e["to"]
    t = e["time"]

    graph[a][b] = t
    graph[b][a] = t


# -----------------------------
# BFS Shortest Path
# -----------------------------
def bfs_shortest_path(start, end):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


# -----------------------------
# Total Travel Time
# -----------------------------
def calculate_total_time(path, edges):
    total = 0

    # Fast lookup table
    time_map = {(e["from"], e["to"]): e["time"] for e in edges}
    time_map.update({(e["to"], e["from"]): e["time"] for e in edges})

    for i in range(len(path) - 1):
        total += time_map[(path[i], path[i + 1])]

    return total



