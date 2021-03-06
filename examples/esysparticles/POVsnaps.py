#POVsnaps.py: Implements an ESyS-Particle runnable for storing
# snapshots of particle simulations rendered using POVray
# Author: D. Weatherley
# Date: 17 May 2007
# Organisation: ESSCC, University of Queensland
# (C) All Rights Reserved, 2007.

from esys.lsm import *
from esys.lsm.util import Vec3, BoundingBox
from esys.lsm.vis import povray

class POVsnaps (Runnable):
    def __init__(self, sim, interval):
        Runnable.__init__(self)
        self.sim = sim
        self.interval = interval
        self.count = 0
        self.configure()

    def configure(
            self,
            lookAt=Vec3(0,0,0),
            camPosn=Vec3(0,0,20),
            zoomFactor=0.1,
            imageSize=[800,600]):
        self.lookAt=lookAt
        self.camPosn=camPosn
        self.zoomFactor=zoomFactor
        self.imageSize=imageSize

    def run(self):
        if ((self.sim.getTimeStep() % self.interval) == 0):
            self.snapshot()
            self.count += 1

    def snapshot(self):
        pkg = povray
        Scene = pkg.Scene()
        plist = self.sim.getParticleList()
        for pp in plist:
            povsphere = pkg.Sphere(pp.getPosn(), pp.getRadius())
            povsphere.apply(pkg.Colors.Red)
            Scene.add(povsphere)
        camera = Scene.getCamera()
        camera.setLookAt(self.lookAt)
        camera.setPosn(self.camPosn)
        camera.setZoom(self.zoomFactor)

        fname = "snap_{0:04d}.png".format(self.count)
        Scene.render(
            offScreen=True,
            interactive=False,
            fileName=fname,
            size=self.imageSize
        )

