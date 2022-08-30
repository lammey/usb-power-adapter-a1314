import bpy

mesh = bpy.data.meshes.new('Rod'+'Mesh')
obj = bpy.data.objects.new('Rod', mesh)
obj.location=(0,0,0)
obj.show_name = False
bpy.context.collection.objects.link(obj)
obj.select_set(True)
vertices = []
faces =[]
vertices.append((0,0,0))
vertices.append((0,2,0))
vertices.append((0,2,2))
vertices.append((0,0,2))
vertices.append((94,0,0))
vertices.append((94,2,0))
vertices.append((94,2,2))
vertices.append((94,0,2))

faces.append([3,2,1,0])
faces.append([4,5,6,7])
faces.append([0,1,5,4])
faces.append([1,2,6,5])
faces.append([2,3,7,6])
faces.append([3,0,4,7])
mesh.from_pydata(vertices, [], faces)
mesh.update()
