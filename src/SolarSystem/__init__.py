"""
SolarSystem - A 3D interactive solar system simulator.

This package provides a Panda3D-based visualization of the solar system
with interactive controls for speed, textures, and camera movement.

Usage:
    python -m SolarSystem.Main

Or as a module:
    from SolarSystem.Main import Main
    app = Main()
    app.run()
"""

__version__ = "1.0.0"
__author__ = "Fock"

# Note: Imports are deferred to avoid import-time side effects with Panda3D
# Use explicit imports when needed:
#   from SolarSystem.Main import Main
