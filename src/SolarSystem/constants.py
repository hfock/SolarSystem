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
# ASSET PATHS
# =============================================================================
MODELS_PATH = "../../models/"
PLANET_MODEL = "planet_sphere"
SKYBOX_MODEL = "solar_sky_sphere"
STARS_TEXTURE = "stars_1k_tex.jpg"
PARTICLE_CONFIG = "fireish.ptf"

# =============================================================================
# PLANET DATA
# Planet configuration: (name, orbit_au, size_scale, year_factor, day_factor, texture)
# orbit_au: Orbital distance in Astronomical Units (Earth = 1.0)
# size_scale: Relative size (Earth = 1.0)
# year_factor: Orbital period relative to Earth year
# day_factor: Rotation period in Earth days
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

# List of planet names for iteration (excludes sun)
PLANET_NAMES = ["sun", "mercury", "venus", "earth", "moon", "mars", "jupiter"]

# Easter egg textures
EASTER_EGG_TEXTURES = {
    "weiss": "weiss.jpg",
    "team": "team.jpg",
    "marm": "marm.jpg",
    "brezina": "brezina.jpg",
    "testbild": "testbild.jpg",
    "borko": "borko.jpg",
}

# Default textures for each planet (for reset)
DEFAULT_TEXTURES = {
    "sun": "sun_1k_tex.jpg",
    "earth": "earth_1k_tex.jpg",
    "moon": "moon_1k_tex.jpg",
    "mars": "mars_1k_tex.jpg",
    "mercury": "mercury_1k_tex.jpg",
    "venus": "venus_1k_tex.jpg",
    "jupiter": "jupiter.jpg",
}

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
