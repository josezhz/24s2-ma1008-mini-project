def load_mrt_data(filename):
    mrt_data = {}  # Dictionary to store station information
    graph = {}  # Graph to store connections

    with open(filename, "r") as file:
        # Skip the first three lines
        for _ in range(3):
            next(file)

        for line in file:
            parts = line.strip().split()  # Split by semicolon
            if len(parts) < 2:
                print(f"Skipping invalid line: {line}")
                continue

            # Extract relevant data from each line
            station_pair = parts[1]
            line_name = parts[2]
            distance = float(parts[3])  # Distance between stations
            first_train = parts[4]
            last_train = parts[5]
            first_train_opposite = parts[6]
            last_train_opposite = parts[7]

            # Extract station codes from the station pair (e.g., "CC1 Dhoby Ghaut <-> CC2 Bras Basah")
            station_a, station_b = station_pair.split(" <-> ")

            # Add station A to mrt_data and graph
            if station_a not in mrt_data:
                mrt_data[station_a] = {
                    "code": station_a.split()[
                        0
                    ],  # The first part is the code (e.g., "CC1")
                    "lines": [line_name],
                    "first_train": first_train,
                    "last_train": last_train,
                    "connections": {},
                }

            # Add station B to mrt_data and graph
            if station_b not in mrt_data:
                mrt_data[station_b] = {
                    "code": station_b.split()[
                        0
                    ],  # The first part is the code (e.g., "CC2")
                    "lines": [line_name],
                    "first_train": first_train_opposite,
                    "last_train": last_train_opposite,
                    "connections": {},
                }

            # Update graph to reflect the connections between station A and B
            graph[station_a] = graph.get(
                station_a,
                {
                    "next": [],
                    "distance": 0,
                    "first_train": first_train,
                    "last_train": last_train,
                },
            )
            graph[station_b] = graph.get(
                station_b,
                {
                    "next": [],
                    "distance": 0,
                    "first_train": first_train_opposite,
                    "last_train": last_train_opposite,
                },
            )

            # Add connections to the graph
            graph[station_a]["next"].append(station_b)
            graph[station_b]["next"].append(station_a)
            graph[station_a]["distance"] = distance
            graph[station_b]["distance"] = distance

    return mrt_data, graph


# Remaining functions (list_stations, find_route, calculate_distance_time, check_train_availability)
# can remain as they are, as they interact with `mrt_data` and `graph` correctly


def list_stations(mrt_data, line_name):
    stations = [
        name for name, details in mrt_data.items() if line_name in details["lines"]
    ]
    print(f"Stations on {line_name} Line:")
    for station in stations:
        print(f"- {station}")
    return stations


from collections import deque


def find_route(graph, start, end):
    queue = deque([(start, [start])])  # (current_station, path_taken)
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path  # Found the shortest path
        if current not in visited:
            visited.add(current)
            for neighbor in graph[current]["next"]:
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found


def calculate_distance_time(graph, start, end, speeds):
    route = find_route(graph, start, end)
    if not route:
        return "No valid route found."

    total_distance = 0
    total_time = 0

    for i in range(len(route) - 1):
        station = route[i]
        next_station = route[i + 1]
        distance = graph[station]["distance"]
        total_distance += distance

        # Find speed for the line (assuming station is on a single line)
        line = list(graph[station]["next"])[0]  # Assume the first line is the main line
        speed = speeds.get(line, 40)  # Default to 40 km/h if not found
        total_time += (distance / speed) * 60  # Convert to minutes

    return f"Total distance: {total_distance:.2f} km\nEstimated travel time: {total_time:.2f} mins"


from datetime import datetime


def check_train_availability(graph, start, current_time, end):
    route = find_route(graph, start, end)
    if not route:
        return "No valid route found."

    last_train_time = datetime.strptime(graph[end]["last_train"], "%H:%M")
    user_time = datetime.strptime(current_time, "%H:%M")

    if user_time > last_train_time:
        return "Sorry, you cannot reach your destination before the last train departs."
    else:
        return "You can complete your journey before the last train."


def main():
    mrt_data, graph = load_mrt_data("MRT.txt")
    speeds = {
        "North-South": 41,
        "East-West": 43,
        "Circle": 36,
        "Thomson-East Coast": 40,
        "North East": 34,
        "Downtown": 38,
    }

    while True:
        print("\nMRT Information System")
        print("1. List all stations on a line")
        print("2. Find best route")
        print("3. Display distance & estimated time")
        print("4. Check train availability")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            line = input("Enter MRT line name: ")
            list_stations(mrt_data, line)

        elif choice == "2":
            start = input("Enter start station: ")
            end = input("Enter destination: ")
            route = find_route(graph, start, end)
            print(" -> ".join(route) if route else "No route found.")

        elif choice == "3":
            start = input("Enter start station: ")
            end = input("Enter destination: ")
            print(calculate_distance_time(graph, start, end, speeds))

        elif choice == "4":
            start = input("Enter start station: ")
            time = input("Enter current time (HH:MM): ")
            end = input("Enter destination: ")
            print(check_train_availability(graph, start, time, end))

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
