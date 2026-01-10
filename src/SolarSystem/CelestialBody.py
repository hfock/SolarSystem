"""
CelestialBody module for SolarSystem application.
Handles loading and animating all planets and celestial objects.
"""

import sys

try:
    from .constants import (
        MODELS_PATH, PLANET_MODEL, PLANETS, SIZE_SCALE, ORBIT_SCALE,
        YEAR_SCALE, DAY_SCALE
    )
except ImportError:
    from constants import (
        MODELS_PATH, PLANET_MODEL, PLANETS, SIZE_SCALE, ORBIT_SCALE,
        YEAR_SCALE, DAY_SCALE
    )


class Planet:
    """
    Represents a single planet or celestial body.

    Handles loading the model, texture, and creating rotation animations.
    Supports custom properties for extensibility (e.g., custom_has_rings, custom_color).
    """

    def __init__(self, name, config, sizescale, orbitscale, yearscale, dayscale, parent_node=None):
        """
        Initialize a planet.

        Args:
            name: Planet name (e.g., "earth", "mars")
            config: Dictionary with planet configuration from constants
            sizescale: Size scaling factor
            orbitscale: Orbit distance scaling factor
            yearscale: Year duration scaling factor
            dayscale: Day duration scaling factor
            parent_node: Parent node for orbit (None for sun, render for most planets)
        """
        self.name = name
        self.config = config
        self.sizescale = sizescale
        self.orbitscale = orbitscale
        self.yearscale = yearscale
        self.dayscale = dayscale
        self.parent_node = parent_node

        # Will be set after loading
        self.model = None
        self.texture = None
        self.orbit_root = None
        self.day_interval = None
        self.orbit_interval = None

        # Preserve custom properties for extensibility
        # Any config key starting with "custom_" is stored as an attribute
        for key, value in config.items():
            if key.startswith("custom_"):
                setattr(self, key, value)

    def load(self):
        """Load the planet model and texture."""
        model_path = f"{MODELS_PATH}{PLANET_MODEL}"
        texture_path = f"{MODELS_PATH}{self.config['texture']}"

        try:
            self.model = loader.loadModel(model_path)
        except Exception as e:
            print(f"Error: Could not load model for {self.name}: {e}")
            sys.exit(1)

        try:
            self.texture = loader.loadTexture(texture_path)
        except Exception as e:
            print(f"Error: Could not load texture for {self.name}: {e}")
            sys.exit(1)

        self.model.setTexture(self.texture, 1)

        # Set size
        size = self.config["size_scale"] * self.sizescale
        self.model.setScale(size)

        # Set up orbit if this planet has one
        if self.config.get("has_orbit", True) and self.config["orbit_au"] > 0:
            self._setup_orbit()
        else:
            # No orbit (e.g., sun) - attach directly to render
            self.model.reparentTo(render)

    def _setup_orbit(self):
        """Set up the orbital node and position."""
        if self.parent_node is None:
            self.parent_node = render

        # Create orbit root node
        orbit_node_name = f"orbit_root_{self.name}"
        self.orbit_root = self.parent_node.attachNewNode(orbit_node_name)

        # Attach planet to orbit root
        self.model.reparentTo(self.orbit_root)

        # Set orbital distance
        orbit_distance = self.config["orbit_au"] * self.orbitscale
        self.model.setPos(orbit_distance, 0, 0)

    def create_animations(self):
        """Create rotation and orbit animations."""
        animations = {}

        # Day rotation (all bodies rotate)
        if self.name == "sun":
            # Sun has special rotation timing
            day_period = self.config["day_factor"]
        else:
            day_period = self.config["day_factor"] * self.dayscale

        self.day_interval = self.model.hprInterval(day_period, (360, 0, 0))
        self.day_interval.loop()
        animations[f"{self.name}Day"] = self.day_interval

        # Orbit animation (if has orbit)
        if self.orbit_root is not None:
            orbit_period = self.config["year_factor"] * self.yearscale
            self.orbit_interval = self.orbit_root.hprInterval(orbit_period, (360, 0, 0))
            self.orbit_interval.loop()
            animations[f"{self.name}Orbit"] = self.orbit_interval

        return animations

    def get_orbit_root(self):
        """Get the orbit root node (for attaching child objects like moons)."""
        return self.orbit_root


class CelestialBody:
    """
    Manager class for all celestial bodies in the solar system.

    Handles loading and rotating all planets using the Planet class.
    """

    def __init__(self, sizescale=SIZE_SCALE, orbitscale=ORBIT_SCALE,
                 yearscale=YEAR_SCALE, dayscale=DAY_SCALE):
        """
        Initialize the celestial body manager.

        Args:
            sizescale: Size scaling factor (default from constants)
            orbitscale: Orbit distance scaling factor (default from constants)
            yearscale: Year duration in seconds (default from constants)
            dayscale: Day duration scaling factor (default from constants)
        """
        self.sizescale = sizescale
        self.orbitscale = orbitscale
        self.dayscale = dayscale
        self.yearscale = yearscale

        # Storage for animations and textures
        self.cbAtt = []  # List of all animation intervals
        self.cbAttDic = {}  # Dictionary: animation_name -> interval
        self.cbAttTex = {}  # Dictionary: planet_name -> model/texture

        # Planet objects
        self.planets = {}
        self.specialSun = None

    def loadAllCelestialBodys(self):
        """Load all celestial bodies defined in constants."""
        # First pass: load all planets except moons
        for planet_config in PLANETS:
            if "parent" not in planet_config:
                self._load_planet(planet_config)

        # Second pass: load moons (which need parent references)
        for planet_config in PLANETS:
            if "parent" in planet_config:
                self._load_moon(planet_config)

    def _load_planet(self, config):
        """
        Load a single planet.

        Args:
            config: Planet configuration dictionary from constants
        """
        name = config["name"]

        planet = Planet(
            name=name,
            config=config,
            sizescale=self.sizescale,
            orbitscale=self.orbitscale,
            yearscale=self.yearscale,
            dayscale=self.dayscale
        )

        planet.load()
        self.planets[name] = planet

        # Store texture and model references
        self.cbAttTex[f"{name}Tex"] = planet.texture
        self.cbAttTex[name] = planet.model

        # Special reference for sun (used by particle effects)
        if name == "sun":
            self.specialSun = planet.model

    def _load_moon(self, config):
        """
        Load a moon (requires parent planet to be loaded first).

        Args:
            config: Moon configuration dictionary from constants
        """
        name = config["name"]
        parent_name = config["parent"]

        if parent_name not in self.planets:
            print(f"Error: Parent planet {parent_name} not found for moon {name}")
            return

        parent_planet = self.planets[parent_name]
        parent_orbit = parent_planet.get_orbit_root()

        # Create moon's orbit root attached to parent's orbit
        moon_orbit_root = parent_orbit.attachNewNode(f"orbit_root_{name}")
        moon_orbit_root.setPos(self.orbitscale, 0, 0)  # Position at parent's orbital distance

        planet = Planet(
            name=name,
            config=config,
            sizescale=self.sizescale,
            orbitscale=self.orbitscale,
            yearscale=self.yearscale,
            dayscale=self.dayscale,
            parent_node=moon_orbit_root
        )

        planet.load()
        self.planets[name] = planet

        # Store texture and model references
        self.cbAttTex[f"{name}Tex"] = planet.texture
        self.cbAttTex[name] = planet.model

    def rotateAllCelestialBodys(self):
        """Create and start animations for all celestial bodies."""
        for name, planet in self.planets.items():
            animations = planet.create_animations()

            for anim_name, interval in animations.items():
                self.cbAtt.append(interval)
                self.cbAttDic[anim_name] = interval
