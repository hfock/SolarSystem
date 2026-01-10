"""
Constants module for SolarSystem application.
Contains all configuration values and magic numbers used throughout the project.
"""

from panda3d.core import VBase4, LVector3

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================
SIZE_SCALE = 0.6          # Planet size multiplier
ORBIT_SCALE = 10          # Orbital distance multiplier
YEAR_SCALE = 60           # Year duration in seconds
DAY_SCALE = YEAR_SCALE / 365.0 * 5  # Day duration

# =============================================================================
# CAMERA SETTINGS
# =============================================================================
CAMERA_POSITION = (0, 0, 45)
CAMERA_ORIENTATION = (0, -90, 0)  # Heading, Pitch, Roll
TRACKBALL_CENTER = (0, 60, 0)

# =============================================================================
# LIGHTING
# =============================================================================
POINT_LIGHT_COLOR = VBase4(0.8, 0.8, 0.8, 1)
POINT_LIGHT_DISTANCE = 3.8
AMBIENT_LIGHT_COLOR = (0.4, 0.4, 0.35, 1)
DIRECTIONAL_LIGHT_DIRECTION = LVector3(0, 8, -2.5)
DIRECTIONAL_LIGHT_COLOR = (0.9, 0.8, 0.9, 1)

# Point light positions (6 lights around origin)
POINT_LIGHT_POSITIONS = [
    (0, 0, POINT_LIGHT_DISTANCE),
    (0, 0, -POINT_LIGHT_DISTANCE),
    (POINT_LIGHT_DISTANCE, 0, 0),
    (-POINT_LIGHT_DISTANCE, 0, 0),
    (0, -POINT_LIGHT_DISTANCE, 0),
    (0, POINT_LIGHT_DISTANCE, 0),
]

# =============================================================================
# SKYBOX
# =============================================================================
SKYBOX_SCALE = 40
BACKGROUND_COLOR = (0, 0, 0)

# =============================================================================
# PROCEDURAL TEXTURES
# =============================================================================
USE_PROCEDURAL_TEXTURES = True  # Enable procedurally generated textures
PROCEDURAL_TEXTURE_RESOLUTION = 512  # Resolution for generated textures (width, higher = slower)
USE_ENHANCED_MATERIALS = True  # Enable enhanced materials and shaders

# =============================================================================
# ASSET PATHS
# =============================================================================
MODELS_PATH = "../../models/"
PLANET_MODEL = "planet_sphere"
SKYBOX_MODEL = "solar_sky_sphere"
STARS_TEXTURE = "stars_1k_tex.jpg"
PARTICLE_CONFIG = "fireish.ptf"

# =============================================================================
# PLANET DATA - Easily Expandable Architecture
# =============================================================================
#
# To add a new celestial body, simply add a dictionary to the PLANETS list below.
# The architecture automatically handles:
#   - Planet name registration
#   - Animation key generation
#   - Texture mapping
#   - Validation
#
# REQUIRED FIELDS:
#   name:         Unique identifier (string)
#   orbit_au:     Orbital distance in AU (0 for sun, relative to parent for moons)
#   size_scale:   Relative size (Earth = 1.0, must be > 0)
#   year_factor:  Orbital period relative to Earth year
#   day_factor:   Rotation period (Earth days, or seconds for sun)
#   texture:      Texture filename in models/ directory (.jpg, .png, .jpeg)
#   has_orbit:    Whether this body orbits (boolean)
#
# OPTIONAL FIELDS:
#   parent:       Parent body name for moons (must be defined earlier in list)
#   moons:        List of moon names (for documentation/future use)
#   custom_*:     Any custom properties for extensions (e.g., custom_color, custom_rings)
#
# EXAMPLE - Adding Saturn with rings and multiple moons:
# {
#     "name": "saturn",
#     "orbit_au": 9.54,
#     "size_scale": 9.14,
#     "year_factor": 29.46,
#     "day_factor": 0.44,
#     "texture": "saturn_1k_tex.jpg",
#     "has_orbit": True,
#     "moons": ["titan", "enceladus"],  # Documentation
#     "custom_has_rings": True,          # Custom property for future extension
# },
# {
#     "name": "titan",
#     "orbit_au": 0.2,  # Relative to Saturn
#     "size_scale": 0.4,
#     "year_factor": 0.044,
#     "day_factor": 0.044,  # Tidally locked
#     "texture": "titan_1k_tex.jpg",
#     "has_orbit": True,
#     "parent": "saturn",  # Must be defined after Saturn
# },
#
# The system automatically:
#   ✓ Validates all required fields on startup
#   ✓ Generates animation keys (saturnDay, saturnOrbit, titanDay, titanOrbit)
#   ✓ Adds to PLANET_NAMES list
#   ✓ Creates DEFAULT_TEXTURES mapping
#   ✓ Handles parent-child relationships for moons
#   ✓ Preserves custom_* properties for extensions
#
# =============================================================================

PLANETS = [
    {
        "name": "sun",
        "orbit_au": 0,
        "size_scale": 2.0,
        "year_factor": 0,
        "day_factor": 20,  # Rotation period in seconds (special case)
        "texture": "sun_1k_tex.jpg",
        "has_orbit": False,
    },
    {
        "name": "mercury",
        "orbit_au": 0.38,
        "size_scale": 0.385,
        "year_factor": 0.241,
        "day_factor": 59,
        "texture": "mercury_1k_tex.jpg",
        "has_orbit": True,
    },
    {
        "name": "venus",
        "orbit_au": 0.72,
        "size_scale": 0.923,
        "year_factor": 0.615,
        "day_factor": 243,
        "texture": "venus_1k_tex.jpg",
        "has_orbit": True,
    },
    {
        "name": "earth",
        "orbit_au": 1.0,
        "size_scale": 1.0,
        "year_factor": 1.0,
        "day_factor": 1.0,
        "texture": "earth_1k_tex.jpg",
        "has_orbit": True,
    },
    {
        "name": "moon",
        "orbit_au": 0.1,  # Relative to Earth
        "size_scale": 0.1,
        "year_factor": 0.0749,
        "day_factor": 0.0749,  # Tidally locked
        "texture": "moon_1k_tex.jpg",
        "has_orbit": True,
        "parent": "earth",
    },
    {
        "name": "mars",
        "orbit_au": 1.52,
        "size_scale": 0.515,
        "year_factor": 1.881,
        "day_factor": 1.03,
        "texture": "mars_1k_tex.jpg",
        "has_orbit": True,
    },
    {
        "name": "jupiter",
        "orbit_au": 2.0,
        "size_scale": 0.923,
        "year_factor": 3.0,
        "day_factor": 23,
        "texture": "jupiter.jpg",
        "has_orbit": True,
    },
]

# =============================================================================
# AUTO-GENERATED DATA STRUCTURES
# These are derived from PLANETS list - DO NOT EDIT MANUALLY
# =============================================================================

def _generate_planet_names():
    """Auto-generate list of planet names from PLANETS configuration."""
    return [planet["name"] for planet in PLANETS]

def _generate_default_textures():
    """Auto-generate default texture mapping from PLANETS configuration."""
    return {planet["name"]: planet["texture"] for planet in PLANETS}

def _generate_planet_animations():
    """Auto-generate animation key mappings for each planet."""
    animations = {}
    for planet in PLANETS:
        name = planet["name"]
        keys = [f"{name}Day"]  # All bodies have day rotation
        if planet.get("has_orbit", True) and planet.get("orbit_au", 0) > 0:
            keys.append(f"{name}Orbit")  # Add orbit if applicable
        animations[name] = keys
    return animations

# Auto-generated from PLANETS list
PLANET_NAMES = _generate_planet_names()
DEFAULT_TEXTURES = _generate_default_textures()
PLANET_ANIMATIONS = _generate_planet_animations()

# Easter egg textures
EASTER_EGG_TEXTURES = {
    "weiss": "weiss.jpg",
    "team": "team.jpg",
    "marm": "marm.jpg",
    "brezina": "brezina.jpg",
    "testbild": "testbild.jpg",
    "borko": "borko.jpg",
}

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_planet_configuration():
    """
    Validate the PLANETS configuration for consistency and completeness.

    Raises:
        ValueError: If configuration is invalid
    """
    required_fields = ["name", "orbit_au", "size_scale", "year_factor",
                      "day_factor", "texture", "has_orbit"]
    planet_names = set()

    for i, planet in enumerate(PLANETS):
        # Check required fields
        for field in required_fields:
            if field not in planet:
                raise ValueError(
                    f"Planet at index {i} missing required field '{field}': {planet}"
                )

        # Check for duplicate names
        name = planet["name"]
        if name in planet_names:
            raise ValueError(f"Duplicate planet name found: '{name}'")
        planet_names.add(name)

        # Validate parent references for moons
        if "parent" in planet:
            parent = planet["parent"]
            if parent not in planet_names:
                raise ValueError(
                    f"Planet '{name}' has parent '{parent}' which is not defined "
                    f"or appears later in PLANETS list. Moons must be defined "
                    f"after their parent planets."
                )

        # Validate numeric fields
        if not isinstance(planet["size_scale"], (int, float)) or planet["size_scale"] <= 0:
            raise ValueError(f"Planet '{name}' has invalid size_scale: {planet['size_scale']}")

        if not isinstance(planet["orbit_au"], (int, float)) or planet["orbit_au"] < 0:
            raise ValueError(f"Planet '{name}' has invalid orbit_au: {planet['orbit_au']}")

        # Validate texture file extension
        if not planet["texture"].lower().endswith(('.jpg', '.png', '.jpeg')):
            raise ValueError(
                f"Planet '{name}' has texture without image extension: {planet['texture']}"
            )

    return True

# Validate configuration on module import
try:
    validate_planet_configuration()
except ValueError as e:
    print(f"CONFIGURATION ERROR: {e}")
    import sys
    sys.exit(1)

# =============================================================================
# UI SETTINGS
# =============================================================================
UI_TEXT_SCALE = 0.05
UI_TITLE_SCALE = 0.07
UI_TEXT_COLOR = (1, 1, 1, 1)

# Key bindings
KEY_BINDINGS = {
    "escape": "exit",
    "space": "toggle_all",
    "+": "speed_up",
    "-": "slow_down",
    "t": "toggle_texture",
    "i": "toggle_instructions",
    "r": "reset",
    "e": "toggle_earth",
    "z": "unlimit",
    "b": "borko_tex",
    "x": "team_tex",
    "y": "marm_tex",
    "c": "brezina_tex",
    "v": "testbild_tex",
}
