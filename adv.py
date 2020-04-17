from room import Room
from player import Player
from world import World

import random
import os
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

# Helper funtion
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

script_dir = os.path.dirname(__file__)
# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(os.path.join(script_dir, map_file), "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Construct a traversal graph
traversal_graph = {}
# Create a stack and push starting vertex
stack = Stack()
stack.push(player.current_room)
# Create a set of traversed vertices
visited = set()
# Create an array for moving to previous room
reverse_path = []
# While queue is not empty
while stack.size() > 0:
    # exit out of the loop if all rooms are visited
    if len(visited) == len(room_graph):
        break

    # pop the first vertex
    current_room = stack.pop()

    # if current room is alread visted, move back
    if current_room.id in visited:
        if len(reverse_path) > 0:
            move_back = reverse_path.pop()
            player.travel(move_back)
            traversal_path.append(move_back)
    # if not visited
    else:
        # push to stack
        stack.push(current_room)
        # Add to traversal graph
        if current_room.id not in traversal_graph:
            traversal_graph[current_room.id] = {}
            for direction in current_room.get_exits():
                traversal_graph[current_room.id][direction] = '?'

        # get random direction that has not been visited
        unvisited = []
        for key in traversal_graph[current_room.id]:
            if traversal_graph[current_room.id][key] == '?':
                unvisited.append(key)
        # if all of the directions are visited, append to visited set
        if len(unvisited) == 0:
            visited.add(current_room.id)
            continue

        # Move to random direction
        random.shuffle(unvisited)
        player.travel(unvisited[0])
        traversal_path.append(unvisited[0])
        # Update graph
        traversal_graph[current_room.id][unvisited[0]] = player.current_room.id
        if player.current_room.id not in traversal_graph:
            traversal_graph[player.current_room.id] = {}
            for direction in player.current_room.get_exits():
                traversal_graph[player.current_room.id][direction] = '?'
        traversal_graph[player.current_room.id][opposite_direction(unvisited[0])] = current_room.id
        stack.push(player.current_room)
        reverse_path.append(opposite_direction(unvisited[0]))

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

