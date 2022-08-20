

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

builder = ml.MeshBuilder('circle')

# Create vertices first
ml.tools.vertCircle(builder=builder, centre=ml.Vec3((0,0,4)), radius=4, vertexCount=256, group='cylinder_top')
ml.tools.vertCircle(builder=builder, centre=ml.Vec3((0,0,0)), radius=4, vertexCount=256, group='cylinder_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,0)), radius=4, height =2, vertexCount=256, group='thread_inner_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,0)), radius=5, height =2, vertexCount=256, group='thread_outer_bottom')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,1)), radius=4, height =2, vertexCount=256, group='thread_inner_top')
ml.tools.vertSpiral(builder=builder, centre=ml.Vec3((0,0,1)), radius=5, height =2, vertexCount=256, group='thread_outer_top')

# Construct faces

# Thread ends
builder.addMultiGroupFace([('thread_inner_bottom', 0), ('thread_outer_bottom', 0), ('thread_outer_top', 0), ('thread_inner_top', 0)])
builder.addMultiGroupFace([('thread_inner_bottom', 255), ('thread_outer_bottom', 255), ('thread_outer_top', 255), ('thread_inner_top', 255)])

# Cyclinder caps
builder.addSpanningFace('cylinder_bottom')
builder.addSpanningFace('cylinder_top')

# Outer thread faces
for i in range(255):
    # Thread outer
    builder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_outer_top', i+1), ('thread_outer_top', i)])
    # Thread bottom
    builder.addMultiGroupFace([('thread_outer_bottom', i), ('thread_outer_bottom', i+1), ('thread_inner_bottom', i+1), ('thread_inner_bottom', i)])
    # Thread inner
    builder.addMultiGroupFace([('thread_inner_bottom', i), ('thread_inner_bottom', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])
    # Thread top
    builder.addMultiGroupFace([('thread_outer_top', i), ('thread_outer_top', i+1), ('thread_inner_top', i+1), ('thread_inner_top', i)])

    # Intervening faces
    builder.addMultiGroupFace([('thread_inner_top', i), ('thread_inner_top', i+1), ('cylinder_top', i+1), ('cylinder_top', i)])
    builder.addMultiGroupFace([('thread_inner_bottom', i), ('thread_inner_bottom', i+1), ('cylinder_bottom', i+1), ('cylinder_bottom', i)])

builder.build()
