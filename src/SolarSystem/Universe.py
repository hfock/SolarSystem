"""
Universe module for SolarSystem application.
Handles environment setup including lighting and skybox.
"""

import sys
from panda3d.core import PointLight, VBase4

try:
    from .constants import (
        POINT_LIGHT_COLOR, POINT_LIGHT_POSITIONS, SKYBOX_SCALE,
        BACKGROUND_COLOR, MODELS_PATH, SKYBOX_MODEL, STARS_TEXTURE
    )
except ImportError:
    from constants import (
        POINT_LIGHT_COLOR, POINT_LIGHT_POSITIONS, SKYBOX_SCALE,
        BACKGROUND_COLOR, MODELS_PATH, SKYBOX_MODEL, STARS_TEXTURE
    )


class Universe:
    """
    Creates and manages the space environment.

    Handles:
    - Point lighting from multiple directions
    - Skybox with star texture
    - Background color
    """

    def __init__(self, base):
        """
        Initialize the Universe.

        Args:
            base: Panda3D ShowBase instance
        """
        self.base = base
        self.sky = None
        self.sky_tex = None
        self.lights = []

        self._init_point_lights()

    def _init_point_lights(self):
        """Set up point lights around the origin for ambient illumination."""
        for i, position in enumerate(POINT_LIGHT_POSITIONS):
            light = PointLight(f'plight_{i}')
            light.setColor(POINT_LIGHT_COLOR)

            light_node = render.attachNewNode(light)
            light_node.setPos(*position)
            render.setLight(light_node)

            self.lights.append(light_node)

        # Set background color and camera look-at
        base.setBackgroundColor(*BACKGROUND_COLOR)
        base.cam.lookAt(0, 0, 0)

    def initSky(self):
        """Load and set up the skybox with star texture."""
        model_path = f"{MODELS_PATH}{SKYBOX_MODEL}"
        texture_path = f"{MODELS_PATH}{STARS_TEXTURE}"

        try:
            self.sky = loader.loadModel(model_path)
        except Exception as e:
            print(f"Error: Could not load skybox model: {e}")
            sys.exit(1)

        try:
            self.sky_tex = loader.loadTexture(texture_path)
        except Exception as e:
            print(f"Error: Could not load sky texture: {e}")
            sys.exit(1)

        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(SKYBOX_SCALE)

    # Legacy method alias
    initPointLight = _init_point_lights
