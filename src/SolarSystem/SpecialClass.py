"""
SpecialClass module for SolarSystem application.
Handles particle effects for the sun.
"""

import sys
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import AmbientLight, DirectionalLight, LVector3, Filename

try:
    from .constants import (
        MODELS_PATH, PARTICLE_CONFIG, AMBIENT_LIGHT_COLOR,
        DIRECTIONAL_LIGHT_DIRECTION, DIRECTIONAL_LIGHT_COLOR
    )
except ImportError:
    from constants import (
        MODELS_PATH, PARTICLE_CONFIG, AMBIENT_LIGHT_COLOR,
        DIRECTIONAL_LIGHT_DIRECTION, DIRECTIONAL_LIGHT_COLOR
    )


class SpecialClass:
    """
    Adds particle effects to the sun for a more realistic appearance.

    Creates a fire-like particle effect emanating from the sun's surface.
    """

    def __init__(self, base, sun):
        """
        Initialize particle effects for the sun.

        Args:
            base: Panda3D ShowBase instance
            sun: The sun's NodePath (model)
        """
        self.base = base
        self.sun = sun
        self.particle_effect = None

        # Enable Panda3D particle system
        base.enableParticles()

        # Set up the sun node for particles
        self.target = sun
        self.target.setPos(0, 0, 0)
        self.target.reparentTo(render)

        # Set up lighting and load particles
        self._setup_lights()
        self._load_particle_config()

    def _setup_lights(self):
        """Set up ambient and directional lighting for particle effects."""
        # Ambient light
        ambient_light = AmbientLight("ambientLight")
        ambient_light.setColor(AMBIENT_LIGHT_COLOR)

        # Directional light
        directional_light = DirectionalLight("directionalLight")
        directional_light.setDirection(DIRECTIONAL_LIGHT_DIRECTION)
        directional_light.setColor(DIRECTIONAL_LIGHT_COLOR)

        # Apply lights to the sun
        self.target.setLight(self.target.attachNewNode(directional_light))
        self.target.setLight(self.target.attachNewNode(ambient_light))

    def _load_particle_config(self):
        """Load and start the particle effect configuration."""
        particle_path = f"{MODELS_PATH}{PARTICLE_CONFIG}"

        try:
            self.particle_effect = ParticleEffect()
            self.particle_effect.loadConfig(Filename(particle_path))
        except Exception as e:
            print(f"Warning: Could not load particle config: {e}")
            return

        # Start particles relative to the sun
        self.particle_effect.start(self.target)
        self.particle_effect.setPos(0, 0, 0)

    def cleanup(self):
        """Clean up particle effects."""
        if self.particle_effect:
            self.particle_effect.cleanup()

    # Legacy method aliases
    setupLights = _setup_lights
    loadParticleConfig = _load_particle_config
