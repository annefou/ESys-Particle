# --- geometry setup script for simple box ---
from gengeo import *

# -- parameters --
# block dimensions
xdim=10
ydim=20
zdim=10

# particle size range
minRadius = 0.2
maxRadius = 1.0
# ---------------------

# corner points
minPoint = Vector3(0.0,0.0,0.0)
maxPoint = Vector3(xdim,ydim,zdim)

# block volume
box = BoxWithPlanes3D(minPoint,maxPoint)

# neighbour table
mntable = MNTable3D(minPoint,maxPoint,2.5*maxRadius,1)

# -- setup packer --
# iteration parameters
insertFails = 1000
maxIter = 1000
tol = 1.0e-6

# packer
packer = InsertGenerator3D(minRadius,maxRadius,insertFails,maxIter,tol)

# pack particles into volume
packer.generatePacking(box,mntable)

# create bonds between neighbouring particles:
mntable.generateBonds(0,1.0e-5,0)

# write a geometry file
mntable.write("box.geo",1)
mntable.write("box.vtu",2)

