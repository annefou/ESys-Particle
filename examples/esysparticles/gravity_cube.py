#gravity_cube.py: A bouncing cube simulation using ESyS-Particle
#Author: D. Weatherley
#Date: 15 May 2007
#Organisation: ESSCC, University of Queensland
#(C) All rights reserved, 2007.
#
#
#import the division module for compatibility between Python 2 and Python 3
from __future__ import division
#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import Vec3, BoundingBox
from esys.lsm.geometry import CubicBlock,ConnectionFinder
from POVsnaps import POVsnaps
#instantiate a simulation object
#and initialise the neighbour search algorithm:
sim = LsmMpi(numWorkerProcesses=1, mpiDimList=[1,1,1])
sim.initNeighbourSearch(
    particleType="NRotSphere",
    gridSpacing=2.5,
    verletDist=0.5
)
#set the number of timesteps and timestep increment:
sim.setNumTimeSteps(10000)
sim.setTimeStepSize(0.001)
#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(-20,-20,-20), Vec3(20,20,20))
sim.setSpatialDomain(domain)
#add a cube of particles to the domain:
cube = CubicBlock(dimCount=[6,6,6], radius=0.5)
cube.rotate(axis=Vec3(0,0,3.141592654/6.0),axisPt=Vec3(0,0,0))
sim.createParticles(cube)
#create bonds between particles separated by less than the specified
#maxDist:
sim.createConnections(
    ConnectionFinder(
        maxDist = 0.005,
        bondTag = 1,
        pList = cube
    )
)
#specify bonded elastic interactions between bonded particles:
bondGrp = sim.createInteractionGroup(
    NRotBondPrms(
        name = "sphereBonds",
        normalK = 10000.0,
        breakDistance = 50.0,
        tag = 1,
        scaling = True
    )
)
#initialise gravity in the domain:
sim.createInteractionGroup(
    GravityPrms(name="earth-gravity", acceleration=Vec3(0,-9.81,0))
)
#add a horizontal wall to act as a floor to bounce particle off:
sim.createWall(
    name="floor",
    posn=Vec3(0,-10,0),
    normal=Vec3(0,1,0)
)
#specify the type of interactions between wall and particles:
sim.createInteractionGroup(
    NRotElasticWallPrms(
        name = "elasticWall",
        wallName = "floor",
        normalK = 10000.0
    )
)
#add local viscosity to simulate air resistance:
sim.createInteractionGroup(
    LinDampingPrms(
        name="linDamping",
        viscosity=0.1,
        maxIterations=100
    )
)
#add a POVsnaps Runnable:
povcam = POVsnaps(sim=sim, interval=100)
povcam.configure(lookAt=Vec3(0,0,0), camPosn=Vec3(14,0,14))
sim.addPostTimeStepRunnable(povcam)
#execute the simulation
sim.run()

