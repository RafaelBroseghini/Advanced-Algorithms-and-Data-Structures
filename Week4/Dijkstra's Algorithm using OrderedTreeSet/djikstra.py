import sys
import turtle
from xml.dom import minidom
from orderedtreeset import OrderedTreeSet
from hashset import HashSet

class Vertex(object):
    def __init__(self,vertexId,x,y,label):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        self.adjacents = []

    def getAdjacents(self, edgeList):
        for e in edgeList:
            if e.v1 == int(self.vertexId):
                self.adjacents.append(e)
            elif e.v2 == int(self.vertexId):
                self.adjacents.append(e)
        return self.adjacents
        
class Edge(object):
    def __init__(self,v1,v2,weight=0):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
    
    def getVertices(self):
        return (self.v1, self.v2)

    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable types")
        return self.weight < other.weight

class Pair(object):
    def __init__(self, vertexId, cost=0):
        self.vertexId = vertexId
        self.cost = cost
    
    def getVertexId(self):
        return self.vertexId

    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable types")
        return self.cost < other.cost

    def __gt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable types")
        return self.cost > other.cost


def djkistra(sourceId: int, vertices:list, vertexDict: dict, edgeList:list):
    # Source pair (root of the OrderedTreeSet.BinaryTree)
    sourcePair = Pair(sourceId, 0)
    
    # visited and unvisited sets.
    # visited = HashSet()
    visited = set()
    unvisited = OrderedTreeSet([sourcePair])

    # build mapping labels -> vertexId & vertexId -> labels
    labelsDict = {int(v.attributes["label"].value):int(v.attributes["vertexId"].value) for v in vertices}
    labels = [labelsDict[i] for i in range(len(labelsDict))]
    previousLabelsDict = {v: k for k, v in labelsDict.items()}

    # build list of distances from sourceId to other vertexIds
    distances = [sys.maxsize for x in range(len(vertices))]
    distances[sourceId] = 0

    # building list of previous
    previous = [-1 for x in range(len(vertices))]
    previous[sourceId] = sourceId

    while len(unvisited) != 0:
        currentPair = unvisited.smallest()
        unvisited.remove(currentPair)

        visited.add(currentPair.getVertexId())

        currentVertex = vertexDict[currentPair.getVertexId()]
        # grab adjacents.
        adjacents = currentVertex.getAdjacents(edgeList)

        for e in adjacents:
            dist = distances[currentVertex.vertexId] + e.weight
            for vertex in [e.v1, e.v2]:
                if vertex not in visited:
                    if distances[vertex] > dist:
                        distances[vertex] = dist
                        previous[vertex] = currentVertex.vertexId
                        unvisited.add(Pair(vertex, dist))

    for i in range(len(visited)):
        print("Vertex:")
        print("  label: {}".format(i))
        print("  cost: {:.2f}".format(distances[labels[i]]))
        print("  previous:{}\n".format(previousLabelsDict[previous[labelsDict[i]]]))

    return previous, distances, labelsDict

def main(start="0"):
    # start = input("What is the source node?: ")
    xmldoc = minidom.parse("graph.xml")
    
    graph = xmldoc.getElementsByTagName("Graph")[0]
    vertices = graph.getElementsByTagName("Vertices")[0].getElementsByTagName("Vertex")
    edges = graph.getElementsByTagName("Edges")[0].getElementsByTagName("Edge")
    
    width = float(graph.attributes["width"].value)
    height = float(graph.attributes["height"].value)

    t = turtle.Turtle()
    screen = t.getscreen()
    screen.setworldcoordinates(0,height,width,0)
    t.speed(1000)
    t.pensize(3)
    t.ht()

    # mapping vertexIds to objects
    vertexDict = {}
    for vertex in vertices:
        vertexId = int(vertex.attributes["vertexId"].value)
        x = float(vertex.attributes["x"].value)
        y = float(vertex.attributes["y"].value)
        label = vertex.attributes["label"].value
        if label == start:
            sourceId = vertexId
        v = Vertex(vertexId, x, y, label)
        vertexDict[vertexId] = v

    # Building list of edges.
    edgeList = []
    
    for edge in edges:
        anEdge = Edge(int(edge.attributes["head"].value), int(edge.attributes["tail"].value))
        if "weight" in edge.attributes:       
            anEdge.weight = float(edge.attributes["weight"].value) 
        edgeList.append(anEdge)

    previous, distances, labelsDict = djkistra(sourceId, vertices, vertexDict, edgeList)

    for edge in edgeList:
        x1 = float(vertexDict[edge.v1].x)
        y1 = float(vertexDict[edge.v1].y)
        x2 = float(vertexDict[edge.v2].x)
        y2 = float(vertexDict[edge.v2].y)
        t.penup()
        t.goto(x1,y1)
        t.pendown()
        t.goto(x2,y2)
        if edge.weight != 0:       
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            t.penup()
            t.goto(x,y)
            t.write(str(edge.weight),align="center",font=("Arial",12,"normal"))
    
    for vertexId in vertexDict:
        t.color("black")
        vertex = vertexDict[vertexId]
        x = vertex.x
        y = vertex.y
        t.penup()
        t.goto(x,y-20)
        
        t.pendown()
        t.fillcolor(0.8,1,0.4)
        t.begin_fill()
        t.circle(20)
        t.end_fill()
        t.penup()
        t.goto(x+2,y+11)
        t.write(vertex.label,align="center",font=("Arial",12,"bold"))

        current = vertexId
        while current != labelsDict[int(start)]:
            c = int(current)
            x1 = float(vertexDict[c].x)
            y1 = float(vertexDict[c].y)
            current = previous[current]
            x2 = float(vertexDict[current].x)
            y2 = float(vertexDict[current].y)
            t.penup()
            t.goto(x1+40,y1-20)
            t.color("purple")
            t.write("{:.2f}".format(distances[c]),align="center",font=("Arial",12,"bold"))
            t.color("red")
            t.goto(x1,y1)
            t.pendown()
            t.goto(x2,y2)
    
    screen.exitonclick()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()