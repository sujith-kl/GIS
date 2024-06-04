class City:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

class QuadTreeNode:
    def __init__(self, bounds):
        self.bounds = bounds
        self.children = [None] * 4
        self.cities = []

MAX_CITIES_PER_NODE = 4

def contains(bounds, coordinates):
    x, y = coordinates
    x1, y1, x2, y2 = bounds
    return x1 <= x <= x2 and y1 <= y <= y2

def intersects(bounds1, bounds2):
    x1, y1, x2, y2 = bounds1
    x3, y3, x4, y4 = bounds2
    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

def is_leaf(node):
    return all(child is None for child in node.children)

def subdivide(node):
    x1, y1, x2, y2 = node.bounds
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    node.children[0] = QuadTreeNode((x1, y1, mx, my))  # NW
    node.children[1] = QuadTreeNode((mx, y1, x2, my))  # NE
    node.children[2] = QuadTreeNode((x1, my, mx, y2))  # SW
    node.children[3] = QuadTreeNode((mx, my, x2, y2))  # SE
    
    cities_to_reinsert = node.cities
    node.cities = []
    for city in cities_to_reinsert:
        insert_city(node, city)

def insert_city(quadtree, city):
    if not contains(quadtree.bounds, city.coordinates):
        return  # City is outside of the bounds, ignore
    if is_leaf(quadtree):
        quadtree.cities.append(city)
        if len(quadtree.cities) > MAX_CITIES_PER_NODE:
            subdivide(quadtree)
    else:
        for child in quadtree.children:
            insert_city(child, city)

def query_range(quadtree, query_bounds):
    result = []
    if not intersects(quadtree.bounds, query_bounds):
        return result
    for city in quadtree.cities:
        if contains(query_bounds, city.coordinates):
            result.append(city)
    if not is_leaf(quadtree):
        for child in quadtree.children:
            result.extend(query_range(child, query_bounds))
    return result

def create_bounds(x1, y1, x2, y2):
    return (x1, y1, x2, y2)

def visualize(quadtree):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots()

    def draw_bounds(bounds):
        x1, y1, x2, y2 = bounds
        width = x2 - x1
        height = y2 - y1
        rect = patches.Rectangle((x1, y1), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    def draw_tree(node):
        if not node:
            return
        draw_bounds(node.bounds)
        for city in node.cities:
            ax.plot(city.coordinates[0], city.coordinates[1], 'bo')
        if not is_leaf(node):
            for child in node.children:
                draw_tree(child)

    draw_tree(quadtree)
    plt.show()

# Example usage
root_bounds = create_bounds(0, 0, 100, 100)
root_node = QuadTreeNode(root_bounds)

# Example list of cities with coordinates
cities = [
    City("Namakkal", (10, 20)),
    City("Salem", (30, 40)),
    City("Karur", (50, 60)),
    City("Erode", (70, 80)),
    City("Kovai", (90, 10))
]

# Insert cities into the quadtree
for city in cities:
    insert_city(root_node, city)

# Example query bounds
query_bounds = create_bounds(0, 0, 70, 70)
cities_in_range = query_range(root_node, query_bounds)
print([city.name for city in cities_in_range])  # Output the names of cities in range

# Visualize the quadtree
visualize(root_node)
