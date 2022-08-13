# This script is ran when the module is loaded

# from .X import Y is a relative import, which is required as the mesh_lib dir itself is not on the module path
from .meshbuilder import *
from .vec3 import *
from .vertexset import *

# This lets us separate tools into a sub-namespace without having to import it explicitly. 
# In the consuming script we can do 'import mesh_lib as ml' then access tools as ml.tools
import mesh_lib.tools as tools