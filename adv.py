from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited = set()
rooms = 0
stack = Stack()
stack.push([player.current_room, None])

while rooms < 500:
    node = stack.pop()
    room = node[0]
    direction = node[1]
    rooms += 1
    if direction != None:
        traversal_path.append(direction)
    visited.add(room.id)
    exits = room.get_exits()
    new_exits = 0
    for item in exits:
        exit_room = room.get_room_in_direction(item)
        if exit_room.id not in visited:
            stack.push([exit_room, item])
            new_exits += 1
    if new_exits == 0:
        q = Queue()
        q.enqueue([room, []])
        bfs_visited = set()
        while q.size() > 0:
            node = q.dequeue()
            current_room = node[0]
            path = node[1]
            if current_room.id not in visited:
                traversal_path += path[:-1]
                stack.push([current_room, path[-1]])
                break
            elif current_room.id not in bfs_visited:
                bfs_visited.add(current_room.id)
                exits = current_room.get_exits()
                for direction in exits:
                    next_room = current_room.get_room_in_direction(direction)
                    q.enqueue([next_room, path + [direction]])

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    print(player.current_room.id)
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
