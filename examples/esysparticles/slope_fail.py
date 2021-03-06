#slope_fail.py: A slope failure simulation using ESyS-Particle
# Author: D. Weatherley
# Date: 23 December 2008
# Organisation: ESSCC, University of Queensland
# (C) All rights reserved, 2008.
#
#
#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *
#instantiate a simulation object
#and initialise the neighbour search algorithm:
sim = LsmMpi (numWorkerProcesses = 1, mpiDimList = [1,1,1])
sim.initNeighbourSearch (
    particleType = "NRotSphere",
    gridSpacing = 2.5000,
    verletDist = 0.1000
)
#specify the number of timesteps and the timestep increment:
sim.setNumTimeSteps (50000)
sim.setTimeStepSize (1.0000e-04)
#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(-20,-20,-20), Vec3(20,20,20))
sim.setSpatialDomain(domain)
#construct a block of particles with radii in range [0.2,0.5]:
geoRandomBlock = RandomBoxPacker (
    minRadius = 0.2000,
    maxRadius = 0.5000,
    cubicPackRadius = 2.2000,
    maxInsertFails = 1000,
    bBox = BoundingBox(
        Vec3(-5.0000, 0.0000,-5.0000),
        Vec3(5.0000, 10.0000, 5.0000)
    ),
    circDimList = [False, False, False],
    tolerance = 1.0000e-05
)
geoRandomBlock.generate()
geoRandomBlock_particles = geoRandomBlock.getSimpleSphereCollection()
#add the particle assembly to the simulation object:
sim.createParticles(geoRandomBlock_particles)
#add a wall as a floor for the model:
sim.createWall (
    name = "floor",
    posn = Vec3(0.0000, 0.0000, 0.0000),
    normal = Vec3(0.0000, 1.0000, 0.0000)
)
#specify that particles undergo unbonded elastic repulsion:
sim.createInteractionGroup (
    NRotElasticPrms (
        name = "repulsion",
        normalK = 1.0000e+03,
        scaling = True
    )
)
#specify that particles undergo elastic repulsion from the floor:
sim.createInteractionGroup (
    NRotElasticWallPrms (
        name = "wall_repell",
        wallName = "floor",
        normalK = 1.0000e+04
    )
)
#specify the direction and magnitude of gravity:
sim.createInteractionGroup (
    GravityPrms (
        name = "gravity",
        acceleration = Vec3(0.0000, -9.8100, 0.0000)
    )
)
#add viscosity to damp particle oscillations:
sim.createInteractionGroup (
    LinDampingPrms (
    name = "viscosity",
        viscosity = 0.1000,
        maxIterations = 100
    )
)
#add a CheckPointer to store simulation data:
sim.createCheckPointer (
    CheckPointPrms (
        fileNamePrefix = "slope_data",
        beginTimeStep = 0,
        endTimeStep = 50000,
        timeStepIncr = 1000
    )
)
#execute the simulation:
sim.run()

