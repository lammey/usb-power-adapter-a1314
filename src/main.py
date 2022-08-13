

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
ml.tools.vertCircle(builder=builder, centre=ml.Vec3((0,0,0)), radius=4, vertexCount=256, group='lower_face')
builder.addSpanningFace('lower_face')
builder.build()