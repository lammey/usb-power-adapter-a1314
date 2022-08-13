from copy import copy, deepcopy

class VertexSet:
    def __init__(self, inList=None, inGroups=None):
        self.vertexList = inList if inList else []
        self.uniqueVerts = {}
        self.groups = inGroups if inGroups else {}
        for i,vertex in enumerate(self.vertexList):
            self.uniqueVerts[vertex]=i

    def addVertex(self, vertex, group = None):
        index = None
        if self.contains(vertex):
            index = self.uniqueVerts[vertex]
        else:
            index = len(self.vertexList)
            self.vertexList.append(vertex)
            self.uniqueVerts[vertex] = index
        
        if group:
            if group not in self.groups:
                self.groups[group] = []
            self.groups[group].append(index)

    # Could have subgroups and such but not in this iteration
    def addGroup(self, name, indices):
        if name in self.groups:
            raise ValueError(f"Group '{name}' already exists in this VertexSet")
        self.groups[name]=indices

    def getVertexAtIndex(self,i):
        return self.vertexList[i]
    
    def contains(self, vertex):
        return vertex in self.uniqueVerts

    def size(self):
        return len(self.vertexList)

    def __add__(self, other):
        # construct sum object to return
        sum = deepcopy(self)

        # vertices
        for vertex in other.vertexList:
            sum.addVertex(vertex)

        # groups    
        for name, group in other.groups.items():
            newGroup = []
            for index in group:
                vertex = other.getVertexAtIndex(index)
                newIndex = index + sum.size()
                if sum.contains(vertex):
                    newIndex = sum.uniqueVerts[vertex]
                newGroup.append(newIndex)
            sum.addGroup(name, newGroup)
        
        return sum
    
    def __deepcopy__(self, memo):
        id_self = id(self)
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = VertexSet(deepcopy(self.vertexList, memo), deepcopy(self.groups, memo))
            memo[id_self] = _copy
        return _copy