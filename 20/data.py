class Path:
    def __init__(self, end=None, path_cost=0):
        self.end = end
        self.path_cost = path_cost

    def __eq__(self, other):
        if not isinstance(other, Path):
            return false
        return self.end == other.end and self.path_cost == other.path_cost

    def __hash__(self):
        return hash(self.end) + hash(self.path_cost)

    def __lt__(self, other):
        if not isinstance(other, Path):
            return False
        return self.path_cost < other.path_cost

class Node:
    def __init__(self, entry=(0,0), name='', neighbors=set()):
        self.entry = entry
        self.name = name
        self.neighbors = neighbors

    def __add__(self, other):
        if not isinstance(other, Node):
            raise RuntimeError("invalid operand")
        return Node(name=self.name, entry=self.entry, neighbors=self.neighbors.union(other.neighbors))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name and self.entry == other.entry

    def __hash__(self):
        return hash(self.entry) + hash(self.name)

class Route:
    def __init__(self, node=None, net_cost=0, via=None):
        self.node = node
        self.net_cost = net_cost
        self.via = via

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        return self.node == other.node

    def __lt__(self, other):
        if not isinstance(other, Route):
            return False
        return self.net_cost < other.net_cost
