import sys
import os
import bpy

# For some reason calls to os.path.realpath(__file__) resolve to C:\main.py
# so we use an env var to resolve path of mesh lib
# Set EXTRA_PYTHON_MODULES to the parent directory of mesh_lib
EXTRA_MODULES='EXTRA_PYTHON_MODULES'
extraModulesPath = os.getenv(EXTRA_MODULES)
if extraModulesPath == None:
    raise Exception(f"Environment variable {EXTRA_MODULES} not defined")
else:
    sys.path.insert(0, extraModulesPath)

import mesh_lib as ml

#-------------------------------------------------------------------------------------#
# Measurements (mm)
#-------------------------------------------------------------------------------------#

SIDES=256
SPIRAL_VERTICES=(2*SIDES)-1
CORE_LENGTH=6
CORE_RADIUS=7
THREAD_RADIUS=7.5
RIM_RADIUS=8
RIM_THICKNESS=0.75
THREAD_GAP=1.15
THREAD_THICKNESS=1.35
LOOP_HEIGHT=THREAD_THICKNESS+THREAD_GAP
CUTOFF_HEIGHT = 1.9
GRIP_HEIGHT=2.5
RIM_THREAD_GAP=1.3
THREAD_START_OFFSET=RIM_THICKNESS+RIM_THREAD_GAP-THREAD_THICKNESS

#-------------------------------------------------------------------------------------#
# Routines
#-------------------------------------------------------------------------------------#

def clean_object(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

#-------------------------------------------------------------------------------------#
# Construction
#-------------------------------------------------------------------------------------#

# Builders
coreBuilder = ml.MeshBuilder('core')
threadBuilder = ml.MeshBuilder('thread')

# Create vertices first
ml.tools.vertCircle(builder=coreBuilder, centre=ml.Vec3((0,0,CORE_LENGTH)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_top')
ml.tools.vertCircle(builder=coreBuilder, centre=ml.Vec3((0,0,-GRIP_HEIGHT)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_START_OFFSET)), radius=CORE_RADIUS-1, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_inner_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_START_OFFSET)), radius=THREAD_RADIUS, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_outer_bottom')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_START_OFFSET+THREAD_THICKNESS)), radius=CORE_RADIUS-1, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_inner_top')
ml.tools.vertSpiral(builder=threadBuilder, centre=ml.Vec3((0,0,THREAD_START_OFFSET+THREAD_THICKNESS)), radius=THREAD_RADIUS, height=LOOP_HEIGHT, loops=2, vertexCount=SIDES, group='thread_outer_top')

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

threadBuilder.build()
bpy.context.view_layer.objects.active = threadBuilder.object
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bisect(plane_co=(0, 0, THREAD_START_OFFSET+THREAD_THICKNESS+CUTOFF_HEIGHT), plane_no=(0, 0, 1), use_fill=True, clear_outer=True)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(plane_co=(0, 0, THREAD_START_OFFSET+THREAD_THICKNESS), plane_no=(0, 0, 1), use_fill=True, clear_inner=True)

coreBuilder.build()

# Merge thread
threadBoolean = coreBuilder.object.modifiers.new(type="BOOLEAN", name="threadBoolean")
threadBoolean.object = threadBuilder.object
threadBoolean.operation = 'UNION'
bpy.context.view_layer.objects.active = coreBuilder.object
bpy.ops.object.modifier_apply(modifier="threadBoolean")
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.remove_doubles()

# Create and merge Rim
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=SIDES, radius=RIM_RADIUS, depth=RIM_THICKNESS, enter_editmode=False, location=(0.0, 0.0, RIM_THICKNESS/2))
bpy.ops.object.select_all(action='DESELECT') # This only works outside edit mode for some reason
cyclinderBoolean = coreBuilder.object.modifiers.new(type="BOOLEAN", name="cylinderBoolean")
cyclinderBoolean.object = bpy.context.scene.objects["Cylinder"]
cyclinderBoolean.operation = 'UNION'
bpy.context.view_layer.objects.active = coreBuilder.object
clean_object(coreBuilder.object)
bpy.ops.object.modifier_apply(modifier="cylinderBoolean")
clean_object(coreBuilder.object)

# Cleanup
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
# bpy.context.view_layer.objects.active=bpy.data.objects['Cylinder']
# bpy.context.view_layer.objects.active=bpy.data.objects['thread']
bpy.data.objects['Cylinder'].select_set(True)
bpy.data.objects['thread'].select_set(True)
# bpy.ops.outliner.delete()
bpy.ops.object.delete()





