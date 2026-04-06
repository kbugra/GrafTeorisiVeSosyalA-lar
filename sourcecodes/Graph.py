graph = {
    "A" : ["B","E"],
    "B" : ["C"],
    "C" : ["D"],
    "D" : ["F"],
    "E" : [],
    "F" : ["H"],
    "G" : ["H"],
    "H" : ["G"],
}
for node in graph:
    print(node, "->", graph[node])

