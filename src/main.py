

import sys
import os

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
builder = ml.MeshBuilder('keyboard_insert')

# Create vertices first
ml.tools.vertCircle(builder=builder, centre=ml.Vec3((0,0,CORE_LENGTH)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_top')
ml.tools.vertCircle(builder=builder, centre=ml.Vec3((0,0,0)), radius=CORE_RADIUS, vertexCount=SIDES, group='core_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,0)), radius=CORE_RADIUS, height=2, loops=2, vertexCount=SIDES, group='thread_inner_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,0)), radius=THREAD_RADIUS, height=2, loops=2, vertexCount=SIDES, group='thread_outer_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,1)), radius=CORE_RADIUS, height=2, loops=2, vertexCount=SIDES, group='thread_inner_top')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,1)), radius=THREAD_RADIUS, height=2, loops=2, vertexCount=SIDES, group='thread_outer_top')

# Construct faces

# Thread ends
builder.addMultiGroupFace([('thread_inner_bottom', 0), ('thread_outer_bottom', 0), ('thread_outer_top', 0), ('thread_inner_top', 0)])
builder.addMultiGroupFace([('thread_inner_bottom', SPIRAL_VERTICES-1), ('thread_outer_bottom', SPIRAL_VERTICES-1), ('thread_outer_top', SPIRAL_VERTICES-1), ('thread_inner_top', SPIRAL_VERTICES-1)])

# Cyclinder caps
builder.addSpanningFace('core_bottom')
builder.addSpanningFace('core_top')

# Outer thread faces
for i in range(SPIRAL_VERTICES-1):
    # Thread outer
    builder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_outer_top', i+1), ('thread_outer_top', i)])
    # Thread bottom
    builder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_inner_bottom', i+1), ('thread_inner_bottom', i)])
    # Thread inner
    builder.addMultiGroupFace([('thread_inner_bottom', i), ('thread_inner_bottom', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])
    # Thread top
    builder.addMultiGroupFace([('thread_outer_top', i), ('thread_outer_top', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])

    # # Intervening faces
    # builder.addMultiGroupFace([('thread_inner_top', i), ('thread_inner_top', i+1), ('core_top', i+1), ('core_top', i)])
    # builder.addMultiGroupFace([('thread_inner_bottom', i), ('thread_inner_bottom', i+1), ('core_bottom', i+1), ('core_bottom', i)])

for i in range(SIDES):
    builder.addMultiGroupFace([('core_bottom', i), ('core_bottom', (i+1)%SIDES), ('core_top', (i+1)%SIDES), ('core_top', i)])
builder.build()
