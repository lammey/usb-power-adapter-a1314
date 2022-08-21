

import sys
import os
import bpy

# For some reason calls to os.path.realpath(__file__) resolve to C:\main.py, so we use an env var to resolve path of mesh lib
# Set EXTRA_PYTHON_MODULES to the parent directory of mesh_lib
EXTRA_MODULES='EXTRA_PYTHON_MODULES'
extraModulesPath = os.getenv(EXTRA_MODULES)
if extraModulesPath == None:
    raise Exception(f"Environment variable {EXTRA_MODULES} not defined")
else:
    sys.path.insert(0, extraModulesPath)

import mesh_lib as ml

SIDES=256
SPIRAL_VERTICES=(2*SIDES)-1

CORE_LENGTH=10
CORE_RADIUS=7
THREAD_RADIUS=7.5
RIM_RADIUS=8
THREAD_THICKNESS=1.35
CUTOFF_HEIGHT = 1.9
LOOP_HEIGHT=THREAD_THICKNESS+1.15

coreBuilder = ml.MeshBuilder('core')
threadBuilder = ml.MeshBuilder('thread')
# Create vertices first
ml.tools.vertCircle(builder=coreBuilder, centre=ml.Vec3((0,0,CORE_LENGTH)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_top')
ml.tools.vertCircle(builder=coreBuilder, centre=ml.Vec3((0,0,-1)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,0)), radius=CORE_RADIUS-1, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_inner_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,0)), radius=THREAD_RADIUS, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_outer_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_THICKNESS)), radius=CORE_RADIUS-1, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_inner_top')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_THICKNESS)), radius=THREAD_RADIUS, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_outer_top')

# Construct faces

# Thread ends
threadBuilder.addMultiGroupFace([('thread_inner_bottom', 0), ('thread_outer_bottom', 0), ('thread_outer_top', 0), ('thread_inner_top', 0)])
threadBuilder.addMultiGroupFace([('thread_inner_bottom', SPIRAL_VERTICES-1), ('thread_outer_bottom', SPIRAL_VERTICES-1), ('thread_outer_top', SPIRAL_VERTICES-1), ('thread_inner_top', SPIRAL_VERTICES-1)])

# Cyclinder caps
coreBuilder.addSpanningFace('core_bottom')
coreBuilder.addSpanningFace('core_top')

# Outer thread faces
for i in range(SPIRAL_VERTICES-1):
    # Thread outer
    threadBuilder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_outer_top', i+1), ('thread_outer_top', i)])
    # Thread bottom
    threadBuilder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_inner_bottom', i+1), ('thread_inner_bottom', i)])
    # Thread inner
    threadBuilder.addMultiGroupFace([('thread_inner_bottom', i), ('thread_inner_bottom', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])
    # Thread top
    threadBuilder.addMultiGroupFace([('thread_outer_top', i), ('thread_outer_top', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])


for i in range(SIDES):
    coreBuilder.addMultiGroupFace([('core_bottom', i), ('core_bottom', (i+1)%SIDES), ('core_top', (i+1)%SIDES), ('core_top', i)])

# coreBuilder.build()
# threadBuilder.build()
# boolean = coreBuilder.object.modifiers.new(type="BOOLEAN", name="booleanXD")
# boolean.object = threadBuilder.object
# boolean.operation = 'UNION'


# bpy.context.view_layer.objects.active = coreBuilder.object
# bpy.ops.object.modifier_apply(modifier="booleanXD")
# bpy.ops.object.mode_set(mode='EDIT')
# bpy.ops.mesh.remove_doubles()

threadBuilder.build()
bpy.context.view_layer.objects.active = threadBuilder.object
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bisect(plane_co=(0, 0, THREAD_THICKNESS+CUTOFF_HEIGHT), plane_no=(0, 0, 1), use_fill=True, clear_outer=True)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(plane_co=(0, 0, THREAD_THICKNESS), plane_no=(0, 0, 1), use_fill=True, clear_inner=True)