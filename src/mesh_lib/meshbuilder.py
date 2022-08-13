from .vertexset import * 
import bpy

# Faces need to be able to be created between arbitrary groups
# so for now only support face creation on this top-level builder object
class MeshBuilder:
    def __init__(self, name):
        self.name = name
        self.vertices = VertexSet()
        self.edges=[]
        self.faces=[]
        self.abstractFaces=[]
    
    def build(self):
        self.resolveFaces()
        mesh = bpy.data.meshes.new(self.name+'Mesh')
        object = bpy.data.objects.new(self.name, mesh)
        object.location=(0,0,0)
        object.show_name = False
        # Link object to scene and make active
        bpy.context.collection.objects.link(object)
        object.select_set(True)
        # Create mesh from given verts, faces.

        mesh.from_pydata(self.vertices.vertexList, self.edges, self.faces)
        # Update mesh with new data
        mesh.update()

    def buildFake(self):
        self.resolveFaces()
        print(self.vertices.vertexList)
        print(self.faces)
        print(len(self.vertices.vertexList))
        print(type(self.vertices.vertexList[0]))
        print(type(self.faces[0]))

    # def addVertexSet(self, vertices):
    #     self.vertices += vertices

    # For faces that span multiple groups
    def addMultiGroupFace(self, face):
        self.abstractFaces.append(face)

    def addFace(self, face, group=None):
        if group:
            new_face = [tuple(group, n) for n in face]
            self.abstractFaces.append(new_face)
        else:
            self.faces.append(face)
        

    def resolveFaces(self):
        for abstractFace in self.abstractFaces:
            concreteFace = self.resolveAbstractFace(abstractFace)
            self.faces.append(concreteFace)

    # For now represent abstract face as a List of tuples [('group_name', 1), ('group_name_2', 4), ...]
    def resolveAbstractFace(self, abstractFace):
        concreteFace = []
        for pair in abstractFace:
            groupName = pair[0]
            index = pair[1]
            # print(f"{groupName} - {index}")
            resolvedIndex = self.vertices.groups[groupName][index]
            concreteFace.append(resolvedIndex)
        return tuple(concreteFace)

    def addSpanningFace(self, group):
        self.faces.append(tuple(self.vertices.groups[group]))

            
    # # Could have subgroups and such but not in this iteration
    # def createGroup(self, name, positions):
    #     self.groups[name] = positions
