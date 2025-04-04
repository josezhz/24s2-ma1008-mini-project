stn_pairs = []
avg_speeds = {
    "North-South": 41,
    "East-West": 43,
    "Circle": 36,
    "Thomson-East Coast": 40,
    "North East": 34,
    "Downtown": 38,
}
stn_neighbors = {}


def load_data():
    file_path = "MRT.txt"
    with open(file_path, "r") as file:  # Automatically closes file
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    data_lines = lines[2:]

    for data_line in data_lines:
        data_list = data_line.split(";")
        from_stn, to_stn = [i.split(" ", 1)[1] for i in data_list[1].split(" <-> ")]
        line = data_list[2]
        distance = float(data_list[3])
        duration = distance / avg_speeds[line]
        first, last, first_opp, last_opp = data_list[4:8]

        stn_pairs.append({
            "from_stn": from_stn,
            "to_stn": to_stn,
            "line": line,
            "distance": distance,
            "duration": duration,
            "first": first,
            "last": last,
            "first_opp": first_opp,
            "last_opp": last_opp
        })

    # Build adjacency list
    for stn_pair in stn_pairs:
        from_stn, to_stn, distance, duration, line = (
            stn_pair["from_stn"],
            stn_pair["to_stn"],
            stn_pair["distance"],
            stn_pair["duration"],
            stn_pair["line"],
        )
        for start, end in [(from_stn, to_stn), (to_stn, from_stn)]:
            stn_neighbors.setdefault(start, {})
            if end not in stn_neighbors[start] or duration < stn_neighbors[start][end]["duration"]:
                stn_neighbors[start][end] = {
                    "distance": distance,
                    "duration": duration,
                    "line": line,
                }


def bellman_ford(graph, start, end):
    if start not in graph or end not in graph:
        return None  # Ensure stations exist in the graph

    distances = {station: float("inf") for station in graph}
    predecessors = {station: None for station in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):  # Relax edges |V|-1 times
        for u in graph:
            for v in graph[u]:
                weight = graph[u][v]["duration"]
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]

    return path[::-1] if path[-1] == start else None  # Reverse path


load_data()
print(bellman_ford(stn_neighbors, "Pioneer", "Punggol"))  # Shortest path based on duration
