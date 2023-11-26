import heapq

class Node:
    def __init__(self, x, y, cost_g=0, cost_h=0):
        self.x = x
        self.y = y
        self.cost_g = cost_g
        self.cost_h = cost_h
        self.cost_f = cost_g + cost_h
        self.parent = None

    def __lt__(self, other):
        return self.cost_f < other.cost_f

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

def heuristic(current, goal):
    return abs(goal.x - current.x) + abs(goal.y - current.y)

def a_star(map_matrix, start, goal, width, height):
    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and map_matrix[y][x] >= 0

    open_set = []
    heapq.heapify(open_set)
    closed_set = set()

    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])

    heapq.heappush(open_set, start_node)

    while open_set:
        current = heapq.heappop(open_set)

        if current.x == goal_node.x and current.y == goal_node.y:
            path = []
            total_cost = current.cost_g
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return total_cost, path[::-1]

        closed_set.add((current.x, current.y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current.x + dx, current.y + dy
            if is_valid(new_x, new_y) and (new_x, new_y) not in closed_set:
                new_node = Node(new_x, new_y, current.cost_g + 1, heuristic(Node(new_x, new_y), goal_node))
                new_node.parent = current
                heapq.heappush(open_set, new_node)

    return None

def read_map(file_path):
    with open(file_path, 'r') as file:
        width, height = map(int, file.readline().split())
        start_x, start_y = map(int, file.readline().split())
        map_matrix = [list(map(int, line.split())) for line in file]

    return width, height, (start_x, start_y), map_matrix

def print_map_with_path(map_matrix, path):
    for i, row in enumerate(map_matrix):
        for j, cell in enumerate(row):
            if (j, i) in path:
                print('X', end=' ')
            else:
                print(cell, end=' ')
        print()

def get_user_input():
    goal_x = int(input("Insira a coordenada X de destino: "))
    goal_y = int(input("Insira a coordenada Y de destino: "))
    return goal_x, goal_y

def main():
    file_path = "C:\\Users\\marci\\OneDrive\\Documentos\\teste\\map.txt"
    width, height, start, map_matrix = read_map(file_path)

    print("Mapa inicial:")
    print_map_with_path(map_matrix, [])

    goal_x, goal_y = get_user_input()

    if not (0 <= goal_x < width and 0 <= goal_y < height):
        print("Coordenadas de destino fora dos limites do mapa. Tente novamente.")
        return

    cost, path = a_star(map_matrix, start, (goal_x, goal_y), width, height) 

    if path:
        print(f"Custo total: {cost}")
        print("Caminho:")
        print(f"{cost} {' '.join([f'{x},{y}' for x, y in path])}")
        print("\nMapa após a escolha das coordenadas:")
        print_map_with_path(map_matrix, path)
    else:
        print("Não foi possível encontrar um caminho.")

if __name__ == "__main__":
    main()

