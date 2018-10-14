from __future__ import print_function
from math import sqrt
import tkinter as tk
import os, sys
import queue

root = tk.Tk()
root.title("Path Finder")
c = tk.Canvas(root, height=400, width=400)
nodesizew = 0
nodesizeh = 0
currentpath = []
closedSet = set()
openSet = set()
graphPos = {}
ROWS = 0
COLS = 0


# Draw graph on GUI
def create_grid(event=None):

    c.delete('grid_line')  # Will only remove the grid_line
    c.delete("all")

    w = c.winfo_width()  # Get current width of canvas
    h = c.winfo_height()
    global nodesizeh
    nodesizeh = (h / ROWS)
    global nodesizew
    nodesizew = (w / COLS)

    # Color the graph and nodes
    for key, value in graphPos.items():
        colorGraph(
            key, {
                '#': 'grey',
                'A': 'red',
                'B': '#00CC00',
                'w': '#4D4DFF',
                'm': '#ABABAB',
                'f': '#116600',
                'g': '#80FF80',
                'r': '#B37700'
            }.get(value, 'white'))

    #  display star, X and circles on the GUI graph
    for i in currentpath:
        c.create_oval(
            i[0] * nodesizew + nodesizew / 3,
            i[1] * nodesizeh + nodesizew / 3, (i[0] * nodesizew) + nodesizew * 2 / 3,
            (i[1] * nodesizeh) + nodesizeh * 2 / 3,
            tag='grid_path',
            fill='black')

    for i in openSet:
        c.create_text(
            i[0] * nodesizew + nodesizew / 2,
            i[1] * nodesizeh + nodesizew / 2,
            tag='grid_path',
            text='★')

    for i in closedSet:
        c.create_text(
            i[0] * nodesizew + nodesizew / 2,
            i[1] * nodesizeh + nodesizew / 2,
            tag='grid_path',
            text='X')


def colorGraph(cord, color):
    c.create_rectangle(
        cord[0] * nodesizew,
        cord[1] * nodesizeh, (cord[0] * nodesizew) + nodesizew,
        (cord[1] * nodesizeh) + nodesizeh,
        tag='grid_line',
        fill=color)


class Graph(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def move_cost(self, a, b):
        return {
            'w': 100,
            'm': 50,
            'f': 10,
            'g': 5,
            'r': 1,
        }.get(graphPos[b], 1)

    def heuristic(self, start, goal):

        # Manhatten Distance
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

        # Dijkstra’s Algorithm
        # return 0

    def in_bounds(self, id):
        # Check walls

        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):

        if (graphPos[id] != '#'):
            return id not in self.walls

    def get_neighbours(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


def A_Star(start, end, graph):

    G = {}
    F = {}

    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedSet = set()
    openSet = set([start])
    cameFrom = {}

    while len(openSet) > 0:
        current = None
        currentFscore = None

        for pos in openSet:

            # Priorrity Queue based on the lowest Fscore
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        if current == end:

            # we found the end!
            # now, return openset, closeset and path from start to end.

            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)

            path.reverse()
            return path, openSet, closedSet

        openSet.remove(current)
        closedSet.add(current)

        for neighbour in graph.get_neighbours(current):
            if neighbour in closedSet:
                continue

            # The distance from start to a neighbor

            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openSet:  # Discover a new node
                openSet.add(neighbour)
            elif candidateG >= G[neighbour]:
                continue  # Not a better path :(

            # best current path
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")


def BFS(start, end, graph):

    cameFrom = {}
    closedSet = set()
    openSet = queue.Queue()
    openSet.put(start)
    closedSet.add(start)

    while openSet.not_empty:

        # Pop Queue
        current = openSet.get()

        if current == end:

            # we found the end! now return openset, closeset
            # and path from start to end

            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)

            path.reverse()

            openSet = set(openSet.queue)
            return path, openSet, closedSet

        for neighbour in graph.get_neighbours(current):

            # chech if neighbour has been visited
            if neighbour not in closedSet:
                cameFrom[neighbour] = current
                openSet.put(neighbour)
                closedSet.add(neighbour)

    raise RuntimeError("BFS failed to find a solution")


if __name__ == "__main__":

    start = (0, 0)
    end = (0, 0)

    # get path to board files
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

    txtpath = os.path.join(dirname, "board-1-3.txt")

    # interpret values of the choosen txt file
    with open(txtpath, "r") as ins:
        x = 0
        y = 0

        for line in ins:
            for ch in line:
                if ch != '\n':
                    graphPos[(x, y)] = ch
                if ch == 'A':
                    start = (x, y)

                if ch == 'B':
                    end = (x, y)
                x += 1
                COLS = x - 1
            y += 1
            x = 0
            ROWS = y

        c.pack(fill=tk.BOTH, expand=True)
        c.bind('<Configure>', create_grid)

        # set geometry values for GUI
        INITNODESIZE = 30
        geom = str(COLS * INITNODESIZE) + 'x' + str(ROWS * INITNODESIZE)
        root.geometry(geom)

        # Run path finder algoritm
        graph = Graph(COLS, ROWS)
        result, openSet, closedSet = A_Star(start, end, graph)
        currentpath = result

    root.mainloop()
