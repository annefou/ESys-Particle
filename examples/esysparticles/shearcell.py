#shearcell.py: An annular shear cell simulation using ESyS-Particle
# Author: D. Weatherley
# Date: 24 April 2011
# Organisation: ESSCC, The University of Queensland, Brisbane, AUSTRALIA
# (C) All rights reserved, 2011.
#
#
#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *
from WallLoader import WallLoaderRunnable
from ServoWallLoader import ServoWallLoaderRunnable
#create a simulation container object:
# N.B. there must be at least two sub-divisions
# in the X-direction for periodic boundaries
sim = LsmMpi (numWorkerProcesses=2, mpiDimList=[2,1,1])
sim.initNeighbourSearch (
    particleType = "NRotSphere",
    gridSpacing = 2.5,
    verletDist = 0.5
)
#specify the number of timesteps and timestep increment:
sim.setNumTimeSteps(100000)
sim.setTimeStepSize(0.001)
#enforce two-dimensional computations:
sim.force2dComputations (True)
#specify the spatial domain and direction of periodic boundaries:
domain = BoundingBox ( Vec3 (0,0,0), Vec3 (10,10,0) )
sim.setSpatialDomain (
    bBox = domain,
    circDimList = [True, False, False]
)
#construct a rectangle of unbonded particles:
packer = RandomBoxPacker (
    minRadius = 0.1,
    maxRadius = 0.5,
    cubicPackRadius = 2.2,
    maxInsertFails = 1000,
    bBox = BoundingBox(
        Vec3(0.0, 0.0,0.0),
        Vec3(10.0, 10.0, 0.0)
    ),
    circDimList = [True, False, False],
    tolerance = 1.0e-5
)
packer.generate()
particleList = packer.getSimpleSphereCollection()
#tag particles along base and top of rectangle
#then add the particles to the simulation object:
for pp in particleList:
    centre = pp.getPosn()
    radius = pp.getRadius()
    Y = centre[1]
    if (Y < 1.0): # particle is near the base (tag=2)
        pp.setTag (2)
    elif (Y > 9.0): # particle is near the top (tag=3)
        pp.setTag (3)
    else: # particle is inside the shear cell (tag=1)
        pp.setTag (1)
    sim.createParticle(pp) # add the particle to the simulation object

#set the density of all particles:
sim.setParticleDensity (
    tag = 1,
    mask = -1,
    Density = 100.0
)
sim.setParticleDensity (
    tag = 2,
    mask = -1,
    Density = 100.0
)
sim.setParticleDensity (
    tag = 3,
    mask = -1,
    Density = 100.0
)
#add driving walls above and below the particle assembly:
sim.createWall (
    name = "bottom_wall",
    posn = Vec3 (0,0,0),
    normal = Vec3 (0,1,0)
)
sim.createWall (
    name = "top_wall",
    posn = Vec3 (0,10,0),
    normal = Vec3 (0,-1,0)
)
#unbonded particle-pairs undergo frictional interactions:
sim.createInteractionGroup (
    NRotFrictionPrms (
        name = "pp_friction",
        normalK = 1000.0,
        dynamicMu = 0.6,
        shearK = 100.0,
        scaling = True
    )
)
#particles near the base (tag=2) are bonded to the bottom wall:
sim.createInteractionGroup (
    NRotBondedWallPrms (
        name = "bwall_bonds",
        wallName = "bottom_wall",
        normalK = 1000.0,
        particleTag = 2
    )
)
#particles near the base (tag=3) are bonded to the top wall:
sim.createInteractionGroup (
    NRotBondedWallPrms (
        name = "twall_bonds",
        wallName = "top_wall",
        normalK = 1000.0,
        particleTag = 3
    )
)
#add local damping to avoid accumulating kinetic energy:
sim.createInteractionGroup (
    LinDampingPrms (
        name = "damping",
        viscosity = 1.0,
        maxIterations = 100
    )
)
#add ServoWallLoaderRunnables to apply constant normal stress:
servo_loader1 = ServoWallLoaderRunnable(
    LsmMpi = sim,
    interactionName = "twall_bonds",
    force = Vec3 (0.0, -1000.0, 0.0),
    startTime = 0,
    rampTime = 5000
)
sim.addPreTimeStepRunnable (servo_loader1)
wall_loader1 = WallLoaderRunnable(
    LsmMpi = sim,
    wallName = "bottom_wall",
    vPlate = Vec3 (0.125, 0.0, 0.0),
    startTime = 30000,
    rampTime = 10000
)
sim.addPreTimeStepRunnable (wall_loader1)
#add a FieldSaver to store total kinetic energy:
sim.createFieldSaver (
    ParticleScalarFieldSaverPrms(
        fieldName="e_kin",
        fileName="ekin.dat",
        fileFormat="SUM",
        beginTimeStep=0,
        endTimeStep=100000,
        timeStepIncr=1
    )
)
#add FieldSavers to store wall forces and positions:
posn_saver = WallVectorFieldSaverPrms(
    wallName=["bottom_wall", "top_wall"],
    fieldName="Position",
    fileName="out_Position.dat",
    fileFormat="RAW_SERIES",
    beginTimeStep=0,
    endTimeStep=100000,
    timeStepIncr=1
)
sim.createFieldSaver(posn_saver)
force_saver = WallVectorFieldSaverPrms(
    wallName=["bottom_wall", "top_wall"],
    fieldName="Force",
    fileName="out_Force.dat",
    fileFormat="RAW_SERIES",
    beginTimeStep=0,
    endTimeStep=100000,
    timeStepIncr=1
)
sim.createFieldSaver(force_saver)
#add a CheckPointer to store simulation data:
sim.createCheckPointer (
    CheckPointPrms (
        fileNamePrefix = "snapshot",
        beginTimeStep = 0,
        endTimeStep = 100000,
        timeStepIncr = 5000
    )
)
#execute the simulation:
sim.run()
