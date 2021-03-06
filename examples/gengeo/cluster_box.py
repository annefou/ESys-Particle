# --- geometry setup script for block with clustered particles ---
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
mntable = MNTable3D(minPoint,maxPoint,2.5*maxRadius,2)

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

# -- set up clustering seeds in a regular grid
# cluster parameters
ncluster_x=3
ncluster_y=6
ncluster_z=3
dx=xdim/float(ncluster_x)
dy=ydim/float(ncluster_y)
dz=zdim/float(ncluster_z)

# regular grid
for i in range(ncluster_x):
    for j in range(ncluster_y):
        for k in range(ncluster_z):
            x=(float(i)+0.5)*dx
            y=(float(j)+0.5)*dy
            z=(float(k)+0.5)*dz
            seed_pos=Vector3(x,y,z)
            tag=i*ncluster_y*ncluster_z+j*ncluster_z+k
            # construct & insert seed "pseudo-particle"
            cseed=Sphere(seed_pos,0.0)
            cseed.setTag(tag)
            mntable.insert(cseed,1)

# -- tag particle according to nearest seed
mntable.tagParticlesToClosest(0,1)

# generate bonds
mntable.generateClusterBonds(0,1.0e-5,1,2)

# remove dummy particles before writing files
mntable.removeParticlesInGroup(1)

# write a geometry file
mntable.write("cluster_box.geo", 1)
mntable.write("cluster_box.vtu", 2)
