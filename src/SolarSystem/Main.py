#!/usr/bin/env python3
"""
Main entry point for the SolarSystem application.
A 3D interactive solar system simulator using Panda3D.

Authors: Fock & Polydor
"""

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

# Use try/except for flexible imports (works both as module and standalone)
try:
    from .CameraHandler import CameraHandler
    from .Universe import Universe
    from .CelestialBody import CelestialBody
    from .ActionHandler import ActionHandler
    from .SpecialClass import SpecialClass
    from .constants import SIZE_SCALE, ORBIT_SCALE, YEAR_SCALE, DAY_SCALE
except ImportError:
    from CameraHandler import CameraHandler
    from Universe import Universe
    from CelestialBody import CelestialBody
    from ActionHandler import ActionHandler
    from SpecialClass import SpecialClass
    from constants import SIZE_SCALE, ORBIT_SCALE, YEAR_SCALE, DAY_SCALE


class Main(DirectObject):
    """
    Main application class for the Solar System simulator.

    Initializes all subsystems:
    - Panda3D rendering engine
    - Camera setup
    - Universe (lighting and skybox)
    - Celestial bodies (sun, planets, moons)
    - User input handling
    - Particle effects
    """

    def __init__(self):
        """Initialize the solar system application."""
        DirectObject.__init__(self)

        # Initialize Panda3D
        self.base = ShowBase()

        # Set up camera
        self.camera_handler = CameraHandler(self.base)

        # Create universe (lighting and skybox)
        self.universe = Universe(self.base)
        self.universe.initSky()

        # Load celestial bodies
        self.celestial_body = CelestialBody(
            sizescale=SIZE_SCALE,
            orbitscale=ORBIT_SCALE,
            yearscale=YEAR_SCALE,
            dayscale=DAY_SCALE
        )
        self.celestial_body.loadAllCelestialBodys()
        self.celestial_body.rotateAllCelestialBodys()

        # Set up user input handling
        self.action_handler = ActionHandler(
            self.base,
            self.celestial_body.cbAttDic,
            self.celestial_body.cbAttTex
        )
        self.action_handler.initAll()

        # Add particle effects to sun
        self.special_effects = SpecialClass(
            self.base,
            self.celestial_body.specialSun
        )

    def run(self):
        """Start the main application loop."""
        self.base.run()


def main():
    """Entry point function."""
    app = Main()
    app.run()


if __name__ == "__main__":
    main()
