import sys
import turtle
from xml.dom import minidom
from orderedtreeset import OrderedTreeSet

class Vertex:
    def __init__(self,vertexId,x,y,label):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        self.adjacents = []
        self.previous = None

    def getAdjacents(self, edgeList):
        for e in edgeList:
            if e.v1 == int(self.vertexId):
                self.adjacents.append(e)
            elif e.v2 == int(self.vertexId):
                self.adjacents.append(e)
        return self.adjacents
        
class Edge:
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
    
    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable types")
        return self.cost < other.cost


def main():
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
        if label == "0":
            sourceId = vertexId
        v = Vertex(vertexId, x, y, label)
        vertexDict[vertexId] = v

    sourcePair = Pair(sourceId, 0)
    # Creating a visited and unvisited set.
    visited = set()
    unvisited = OrderedTreeSet([sourcePair])
    # Building list of edges.
    edgeList = []
    
    for edge in edges:
        anEdge = Edge(int(edge.attributes["head"].value), int(edge.attributes["tail"].value))
        if "weight" in edge.attributes:       
            anEdge.weight = float(edge.attributes["weight"].value) 
        edgeList.append(anEdge)

    # build labels
    labelsDict = {int(v.attributes["label"].value):int(v.attributes["vertexId"].value) for v in vertices}
    labels = [labelsDict[i] for i in range(len(labelsDict))]

    # build list of distances from sourceId to other vertexIds
    distances = [sys.maxsize for x in range(len(vertices))]
    distances[sourceId] = 0

    # building list of previous
    previous = [-1 for x in range(len(vertices))]
    previous[sourceId] = sourceId
    previousLabelsDict = {v: k for k, v in labelsDict.items()}

    # get adjacents of sourceId
    while len(unvisited) != 0:
        current = unvisited.tree.getSmallest()
        unvisited.remove(current.getVal())

        visited.add(current.getValId())

        currentVertex = vertexDict[current.getValId()]
        # grab adjacents.
        adjacents = currentVertex.getAdjacents(edgeList)

        for e in adjacents:
            if e.v1 not in visited:
                dist = distances[currentVertex.vertexId] + e.weight
                if distances[e.v1] > dist:
                    distances[e.v1] = dist
                    previous[e.v1] = currentVertex.vertexId
                    unvisited.add(Pair(e.v1, dist))
            if e.v2 not in visited:
                dist = distances[currentVertex.vertexId] + e.weight
                if distances[e.v2] > dist:
                    distances[e.v2] = dist
                    previous[e.v2] = currentVertex.vertexId
                    unvisited.add(Pair(e.v2, dist))


    for i in range(len(visited)):
        print("Vertex:")
        print("  label: {}".format(i))
        print("  cost: {:.2f}".format(distances[labels[i]]))
        print("  previous:{}\n".format(previousLabelsDict[previous[labelsDict[i]]])) 

    print(previous)

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
        while current != 15:
            c = int(current)
            x1 = float(vertexDict[c].x)
            y1 = float(vertexDict[c].y)
            current = previous[current]
            x2 = float(vertexDict[current].x)
            y2 = float(vertexDict[current].y)
            t.color("red")
            t.penup()
            t.goto(x1,y1)
            t.pendown()
            t.goto(x2,y2)
    
    screen.exitonclick()


if __name__ == '__main__':
    main()