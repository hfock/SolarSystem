"""
CameraHandler module for SolarSystem application.
Handles camera positioning and trackball setup.
"""

try:
    from .constants import CAMERA_POSITION, CAMERA_ORIENTATION, TRACKBALL_CENTER
except ImportError:
    from constants import CAMERA_POSITION, CAMERA_ORIENTATION, TRACKBALL_CENTER


class CameraHandler:
    """
    Sets up and manages the camera for viewing the solar system.

    Configures:
    - Initial camera position (top-down view)
    - Camera orientation
    - Trackball for mouse-controlled rotation
    """

    def __init__(self, base):
        """
        Initialize the camera handler.

        Args:
            base: Panda3D ShowBase instance
        """
        self.base = base

        # Set camera position (top-down view)
        camera.setPos(*CAMERA_POSITION)

        # Set camera orientation (looking down at the solar system)
        camera.setHpr(*CAMERA_ORIENTATION)

        # Set up trackball for mouse control
        self.base.trackball.node().setPos(*TRACKBALL_CENTER)
