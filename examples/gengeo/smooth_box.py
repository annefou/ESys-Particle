# --- geometry setup script for block with smooth sides ---
from gengeo import *

# - input parameters --
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

# neighbour table
mntable = MNTable3D(minPoint,maxPoint,2.5*maxRadius,1)

# block volume
box = BoxWithPlanes3D(minPoint,maxPoint)

# boundary planes
bottomPlane=Plane(minPoint,Vector3(0.0,1.0,0.0))
leftPlane=Plane(minPoint,Vector3(1.0,0.0,0.0))
frontPlane=Plane(minPoint,Vector3(0.0,0.0,1.0))
topPlane=Plane(maxPoint,Vector3(0.0,-1.0,0.0))
rightPlane=Plane(maxPoint,Vector3(-1.0,0.0,0.0))
backPlane=Plane(maxPoint,Vector3(0.0,0.0,-1.0))

# add them to the box
box.addPlane(bottomPlane)
box.addPlane(leftPlane)
box.addPlane(frontPlane)
box.addPlane(topPlane)
box.addPlane(rightPlane)
box.addPlane(backPlane)

# -- setup packer --
# iteration parameters
insertFails = 1000
maxIter = 1000
tol = 1.0e-6

# packer
packer = InsertGenerator3D( minRadius,maxRadius,insertFails,maxIter,tol,False)

# pack particles into volume
packer.generatePacking(box,mntable,0,1)

# create bonds between neighbouring particles:
mntable.generateBonds(0,1.0e-5,0)

# calculate and print the porosity:
volume = xdim*ydim*zdim
porosity = (volume - mntable.getSumVolume(groupID=0))/volume
print "Porosity: ", porosity

# write a geometry file
mntable.write("smooth_box.geo", 1)
mntable.write("smooth_box.vtu", 2)

