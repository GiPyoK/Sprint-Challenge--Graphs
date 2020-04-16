from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

# Helper funtions
def opposite_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'
    else:
        return None

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Create a Q and enqueue starting vertex
qq = Queue()
qq.enqueue(player.current_room)
# Create a set of traversed vertices
visited = set()
# Create a traversal graph
traversal_graph = {}
# While queue is not empty
while qq.size() > 0:
    # dequeue/pop the first vertex
    current_room = qq.dequeue()
    player.current_room = current_room
    # if not visited
    if current_room.id not in visited:
        # Add to traversal graph
        if current_room.id not in traversal_graph:
            traversal_graph[current_room.id] = {}
        # Mark as visited
        visited.add(current_room.id)
        # enqueue all neighbors
        for direction in current_room.get_exits():
            # Move to exit
            player.travel(direction)
            # Record the path
            traversal_graph[current_room.id][direction] = player.current_room.id
            # Enqueue exits that are not yet visited (BFT)
            if player.current_room.id not in visited:
                qq.enqueue(player.current_room)
            # Move back to previous room
            player.travel(opposite_direction(direction))

breakpoint()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
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

