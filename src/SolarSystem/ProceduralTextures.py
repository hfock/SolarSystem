"""
Procedural Texture Generation Module for Solar System
Generates beautiful, realistic textures for planets using noise algorithms.
"""

import numpy as np
from panda3d.core import Texture, PNMImage
from enum import Enum
import random


class PlanetType(Enum):
    """Types of celestial bodies for texture generation"""
    TERRESTRIAL = "terrestrial"  # Rocky planets like Earth, Mars
    GAS_GIANT = "gas_giant"      # Gas giants like Jupiter, Saturn
    ICE_GIANT = "ice_giant"      # Ice giants like Uranus, Neptune
    ROCKY = "rocky"              # Rocky/barren like Mercury, Moon
    STAR = "star"                # Stars like the Sun


class PerlinNoise:
    """Perlin noise generator for natural-looking textures"""

    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)

        # Create permutation table
        self.p = np.arange(256, dtype=int)
        np.random.shuffle(self.p)
        self.p = np.concatenate([self.p, self.p])

    def fade(self, t):
        """Fade function for smooth interpolation"""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        """Linear interpolation"""
        return a + t * (b - a)

    def grad(self, hash_val, x, y):
        """Gradient function"""
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x, y):
        """Generate 2D Perlin noise at coordinates (x, y)"""
        # Grid cell coordinates
        xi = int(np.floor(x)) & 255
        yi = int(np.floor(y)) & 255

        # Fractional coordinates
        xf = x - np.floor(x)
        yf = y - np.floor(y)

        # Fade curves
        u = self.fade(xf)
        v = self.fade(yf)

        # Hash coordinates of the 4 corners
        aa = self.p[self.p[xi] + yi]
        ab = self.p[self.p[xi] + yi + 1]
        ba = self.p[self.p[xi + 1] + yi]
        bb = self.p[self.p[xi + 1] + yi + 1]

        # Blend results from corners
        x1 = self.lerp(u, self.grad(aa, xf, yf), self.grad(ba, xf - 1, yf))
        x2 = self.lerp(u, self.grad(ab, xf, yf - 1), self.grad(bb, xf - 1, yf - 1))

        return self.lerp(v, x1, x2)

    def fbm(self, x, y, octaves=6, persistence=0.5, lacunarity=2.0):
        """Fractional Brownian Motion - layered noise for more detail"""
        total = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0

        for _ in range(octaves):
            total += self.noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity

        return total / max_value


class ProceduralTextureGenerator:
    """Main class for generating procedural planet textures"""

    def __init__(self, width=1024, height=512, seed=None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        self.noise = PerlinNoise(seed=self.seed)

    def _create_pnm_image(self):
        """Create a new PNMImage for texture generation"""
        img = PNMImage(self.width, self.height)
        img.fill(0, 0, 0)
        return img

    def _spherical_mapping(self, u, v):
        """Convert UV coordinates to spherical coordinates for better planet mapping"""
        theta = u * 2 * np.pi  # Longitude
        phi = v * np.pi        # Latitude

        # Convert to 3D coordinates for better noise sampling
        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)

        return x, y, z

    def generate_terrestrial_texture(self, land_color=(0.3, 0.5, 0.2), ocean_color=(0.1, 0.2, 0.5),
                                    mountain_color=(0.5, 0.4, 0.3), ice_color=(0.9, 0.9, 1.0)):
        """Generate Earth-like terrestrial planet texture"""
        img = self._create_pnm_image()

        progress_interval = max(1, self.height // 10)  # Show progress every 10%

        for y in range(self.height):
            if y % progress_interval == 0 and y > 0:
                progress = int((y / self.height) * 100)
                print(f"  Progress: {progress}%")

            for x in range(self.width):
                u = x / self.width
                v = y / self.height

                # Spherical mapping for better planet appearance
                sx, sy, sz = self._spherical_mapping(u, v)

                # Multiple noise layers for complex terrain
                continents = self.noise.fbm(sx * 3, sy * 3, octaves=4, persistence=0.6)
                terrain = self.noise.fbm(sx * 8, sy * 8, octaves=6, persistence=0.5)
                detail = self.noise.fbm(sx * 20, sy * 20, octaves=4, persistence=0.4)

                # Water threshold
                water_level = -0.1

                # Determine color based on elevation
                if continents < water_level:
                    # Ocean
                    depth = (water_level - continents) * 3
                    r = ocean_color[0] * (1 - depth * 0.3)
                    g = ocean_color[1] * (1 - depth * 0.3)
                    b = ocean_color[2] * (1 - depth * 0.1)
                else:
                    # Land
                    elevation = continents + terrain * 0.3 + detail * 0.1

                    # Ice caps at poles
                    pole_factor = abs(v - 0.5) * 2  # 0 at equator, 1 at poles
                    ice_threshold = 0.7

                    if pole_factor > ice_threshold:
                        # Ice
                        ice_mix = (pole_factor - ice_threshold) / (1 - ice_threshold)
                        r = land_color[0] * (1 - ice_mix) + ice_color[0] * ice_mix
                        g = land_color[1] * (1 - ice_mix) + ice_color[1] * ice_mix
                        b = land_color[2] * (1 - ice_mix) + ice_color[2] * ice_mix
                    elif elevation > 0.5:
                        # Mountains
                        mount_mix = min((elevation - 0.5) * 2, 1.0)
                        r = land_color[0] * (1 - mount_mix) + mountain_color[0] * mount_mix
                        g = land_color[1] * (1 - mount_mix) + mountain_color[1] * mount_mix
                        b = land_color[2] * (1 - mount_mix) + mountain_color[2] * mount_mix
                    else:
                        # Regular land
                        r, g, b = land_color[0], land_color[1], land_color[2]
                        # Add variation
                        r += terrain * 0.1
                        g += terrain * 0.15
                        b += terrain * 0.05

                # Add atmospheric scattering effect
                atmosphere_effect = 1.0 + np.sin(v * np.pi) * 0.1

                # Clamp and set pixel
                r = max(0, min(1, r * atmosphere_effect))
                g = max(0, min(1, g * atmosphere_effect))
                b = max(0, min(1, b * atmosphere_effect))

                img.set_xel(x, y, r, g, b)

        print("  Progress: 100%")
        return self._convert_to_texture(img)

    def generate_gas_giant_texture(self, primary_color=(0.8, 0.6, 0.4),
                                   secondary_color=(0.9, 0.8, 0.6),
                                   storm_color=(0.9, 0.3, 0.2)):
        """Generate Jupiter/Saturn-like gas giant texture with bands and storms"""
        img = self._create_pnm_image()

        progress_interval = max(1, self.height // 10)  # Show progress every 10%

        for y in range(self.height):
            if y % progress_interval == 0 and y > 0:
                progress = int((y / self.height) * 100)
                print(f"  Progress: {progress}%")

            for x in range(self.width):
                u = x / self.width
                v = y / self.height

                # Horizontal bands (latitudinal)
                bands = np.sin(v * 20 + self.noise.fbm(u * 5, v * 2, octaves=3) * 2) * 0.5 + 0.5

                # Turbulence for storm patterns
                turbulence = self.noise.fbm(u * 8, v * 15, octaves=6, persistence=0.6)

                # Great red spot effect (add a storm)
                storm_center_x = 0.7
                storm_center_y = 0.4
                dist_to_storm = np.sqrt((u - storm_center_x)**2 + (v - storm_center_y)**2 * 4)
                storm_intensity = max(0, 1 - dist_to_storm * 8) * 0.7

                # Swirl pattern in storm
                if storm_intensity > 0:
                    angle = np.arctan2(v - storm_center_y, u - storm_center_x)
                    swirl = self.noise.fbm(u * 10 + np.cos(angle) * storm_intensity * 3,
                                          v * 10 + np.sin(angle) * storm_intensity * 3,
                                          octaves=4)
                    storm_intensity *= (swirl * 0.5 + 0.5)

                # Mix colors based on bands and turbulence
                band_mix = bands + turbulence * 0.3
                band_mix = max(0, min(1, band_mix))

                r = primary_color[0] * (1 - band_mix) + secondary_color[0] * band_mix
                g = primary_color[1] * (1 - band_mix) + secondary_color[1] * band_mix
                b = primary_color[2] * (1 - band_mix) + secondary_color[2] * band_mix

                # Add storm coloring
                if storm_intensity > 0:
                    r = r * (1 - storm_intensity) + storm_color[0] * storm_intensity
                    g = g * (1 - storm_intensity) + storm_color[1] * storm_intensity
                    b = b * (1 - storm_intensity) + storm_color[2] * storm_intensity

                # Add fine detail
                detail = self.noise.fbm(u * 30, v * 30, octaves=3, persistence=0.3) * 0.1
                r += detail
                g += detail
                b += detail

                # Clamp and set pixel
                r = max(0, min(1, r))
                g = max(0, min(1, g))
                b = max(0, min(1, b))

                img.set_xel(x, y, r, g, b)

        print("  Progress: 100%")
        return self._convert_to_texture(img)

    def generate_rocky_texture(self, base_color=(0.5, 0.4, 0.35),
                               crater_color=(0.3, 0.25, 0.2)):
        """Generate Moon/Mercury-like rocky, cratered texture"""
        img = self._create_pnm_image()

        progress_interval = max(1, self.height // 10)  # Show progress every 10%

        for y in range(self.height):
            if y % progress_interval == 0 and y > 0:
                progress = int((y / self.height) * 100)
                print(f"  Progress: {progress}%")

            for x in range(self.width):
                u = x / self.width
                v = y / self.height

                sx, sy, sz = self._spherical_mapping(u, v)

                # Base rocky terrain
                terrain = self.noise.fbm(sx * 10, sy * 10, octaves=6, persistence=0.5)
                detail = self.noise.fbm(sx * 25, sy * 25, octaves=4, persistence=0.4)

                # Create craters
                crater_noise = self.noise.fbm(sx * 15, sy * 15, octaves=3, persistence=0.6)
                craters = 0

                # Add multiple crater layers
                for i in range(5):
                    crater_x = (sx + i * 0.3) * 8
                    crater_y = (sy + i * 0.3) * 8
                    crater_pattern = self.noise.noise(crater_x, crater_y)

                    if crater_pattern > 0.7:
                        crater_depth = (crater_pattern - 0.7) * 3
                        craters += crater_depth

                # Combine all elements
                elevation = terrain * 0.6 + detail * 0.2 - craters * 0.4

                # Color based on elevation
                color_mix = max(0, min(1, (elevation + 1) / 2))

                r = base_color[0] * color_mix + crater_color[0] * (1 - color_mix)
                g = base_color[1] * color_mix + crater_color[1] * (1 - color_mix)
                b = base_color[2] * color_mix + crater_color[2] * (1 - color_mix)

                # Add variation
                r += detail * 0.1
                g += detail * 0.1
                b += detail * 0.1

                # Clamp and set pixel
                r = max(0, min(1, r))
                g = max(0, min(1, g))
                b = max(0, min(1, b))

                img.set_xel(x, y, r, g, b)

        print("  Progress: 100%")
        return self._convert_to_texture(img)

    def generate_ice_giant_texture(self, base_color=(0.3, 0.5, 0.7),
                                   cloud_color=(0.6, 0.75, 0.9)):
        """Generate Uranus/Neptune-like ice giant texture"""
        img = self._create_pnm_image()

        progress_interval = max(1, self.height // 10)  # Show progress every 10%

        for y in range(self.height):
            if y % progress_interval == 0 and y > 0:
                progress = int((y / self.height) * 100)
                print(f"  Progress: {progress}%")

            for x in range(self.width):
                u = x / self.width
                v = y / self.height

                # Subtle bands
                bands = np.sin(v * 12 + self.noise.fbm(u * 3, v * 1.5, octaves=2) * 1.5) * 0.5 + 0.5

                # Smooth cloud patterns
                clouds = self.noise.fbm(u * 6, v * 6, octaves=5, persistence=0.5)

                # Very subtle features (ice giants are more uniform)
                features = self.noise.fbm(u * 15, v * 15, octaves=3, persistence=0.3) * 0.1

                # Mix colors
                mix = (bands * 0.4 + clouds * 0.4 + 0.2) + features
                mix = max(0, min(1, mix))

                r = base_color[0] * (1 - mix) + cloud_color[0] * mix
                g = base_color[1] * (1 - mix) + cloud_color[1] * mix
                b = base_color[2] * (1 - mix) + cloud_color[2] * mix

                # Subtle atmospheric gradient
                atmosphere_gradient = 1.0 + np.sin(v * np.pi) * 0.05

                r *= atmosphere_gradient
                g *= atmosphere_gradient
                b *= atmosphere_gradient

                # Clamp and set pixel
                r = max(0, min(1, r))
                g = max(0, min(1, g))
                b = max(0, min(1, b))

                img.set_xel(x, y, r, g, b)

        print("  Progress: 100%")
        return self._convert_to_texture(img)

    def generate_star_texture(self, base_color=(1.0, 0.9, 0.6)):
        """Generate Sun-like star texture with surface detail"""
        img = self._create_pnm_image()

        progress_interval = max(1, self.height // 10)  # Show progress every 10%

        for y in range(self.height):
            if y % progress_interval == 0 and y > 0:
                progress = int((y / self.height) * 100)
                print(f"  Progress: {progress}%")

            for x in range(self.width):
                u = x / self.width
                v = y / self.height

                sx, sy, sz = self._spherical_mapping(u, v)

                # Turbulent surface
                turbulence = self.noise.fbm(sx * 5, sy * 5, octaves=6, persistence=0.6)

                # Granulation pattern
                granules = self.noise.fbm(sx * 20, sy * 20, octaves=4, persistence=0.4) * 0.3

                # Sunspots
                spots = self.noise.fbm(sx * 8, sy * 8, octaves=3, persistence=0.5)
                sunspot = 0
                if spots < -0.5:
                    sunspot = (-0.5 - spots) * 1.5

                # Combine effects
                brightness = 0.8 + turbulence * 0.15 + granules - sunspot * 0.4
                brightness = max(0.3, min(1.2, brightness))

                r = base_color[0] * brightness
                g = base_color[1] * brightness
                b = base_color[2] * brightness

                # Clamp and set pixel
                r = max(0, min(1, r))
                g = max(0, min(1, g))
                b = max(0, min(1, b))

                img.set_xel(x, y, r, g, b)

        print("  Progress: 100%")
        return self._convert_to_texture(img)

    def _convert_to_texture(self, pnm_image):
        """Convert PNMImage to Panda3D Texture"""
        texture = Texture()
        texture.load(pnm_image)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        texture.setWrapU(Texture.WMRepeat)
        texture.setWrapV(Texture.WMClamp)
        return texture


# Planet-specific texture generators with custom color schemes
PLANET_CONFIGS = {
    "sun": {
        "type": PlanetType.STAR,
        "base_color": (1.0, 0.85, 0.5)
    },
    "mercury": {
        "type": PlanetType.ROCKY,
        "base_color": (0.5, 0.45, 0.4),
        "crater_color": (0.35, 0.3, 0.25)
    },
    "venus": {
        "type": PlanetType.TERRESTRIAL,
        "land_color": (0.8, 0.7, 0.4),
        "ocean_color": (0.75, 0.65, 0.35),  # No oceans, but used for lowlands
        "mountain_color": (0.85, 0.8, 0.5),
        "ice_color": (0.9, 0.85, 0.6)
    },
    "earth": {
        "type": PlanetType.TERRESTRIAL,
        "land_color": (0.2, 0.5, 0.15),
        "ocean_color": (0.05, 0.15, 0.4),
        "mountain_color": (0.4, 0.35, 0.3),
        "ice_color": (0.95, 0.95, 1.0)
    },
    "moon": {
        "type": PlanetType.ROCKY,
        "base_color": (0.6, 0.6, 0.55),
        "crater_color": (0.4, 0.4, 0.35)
    },
    "mars": {
        "type": PlanetType.TERRESTRIAL,
        "land_color": (0.7, 0.3, 0.1),
        "ocean_color": (0.5, 0.25, 0.15),  # Dried ocean beds
        "mountain_color": (0.6, 0.25, 0.1),
        "ice_color": (0.95, 0.9, 0.85)
    },
    "jupiter": {
        "type": PlanetType.GAS_GIANT,
        "primary_color": (0.75, 0.55, 0.35),
        "secondary_color": (0.85, 0.75, 0.6),
        "storm_color": (0.9, 0.35, 0.2)
    },
    "saturn": {
        "type": PlanetType.GAS_GIANT,
        "primary_color": (0.85, 0.75, 0.5),
        "secondary_color": (0.9, 0.85, 0.7),
        "storm_color": (0.95, 0.8, 0.6)
    },
    "uranus": {
        "type": PlanetType.ICE_GIANT,
        "base_color": (0.4, 0.65, 0.75),
        "cloud_color": (0.6, 0.8, 0.85)
    },
    "neptune": {
        "type": PlanetType.ICE_GIANT,
        "base_color": (0.2, 0.35, 0.7),
        "cloud_color": (0.4, 0.5, 0.8)
    }
}


def generate_texture_for_planet(planet_name, resolution=1024, seed=None):
    """
    Generate a procedural texture for a specific planet.

    Args:
        planet_name: Name of the planet (e.g., "earth", "jupiter")
        resolution: Texture resolution (width will be resolution, height will be resolution/2)
        seed: Random seed for reproducible textures

    Returns:
        Panda3D Texture object
    """
    planet_name_lower = planet_name.lower()

    if planet_name_lower not in PLANET_CONFIGS:
        print(f"Warning: No procedural config for {planet_name}, using rocky texture")
        config = {"type": PlanetType.ROCKY}
    else:
        config = PLANET_CONFIGS[planet_name_lower]

    # Use planet-specific seed if none provided
    if seed is None:
        seed = hash(planet_name_lower) % 1000000

    generator = ProceduralTextureGenerator(width=resolution, height=resolution // 2, seed=seed)

    planet_type = config["type"]

    if planet_type == PlanetType.STAR:
        return generator.generate_star_texture(
            base_color=config.get("base_color", (1.0, 0.9, 0.6))
        )
    elif planet_type == PlanetType.TERRESTRIAL:
        return generator.generate_terrestrial_texture(
            land_color=config.get("land_color", (0.3, 0.5, 0.2)),
            ocean_color=config.get("ocean_color", (0.1, 0.2, 0.5)),
            mountain_color=config.get("mountain_color", (0.5, 0.4, 0.3)),
            ice_color=config.get("ice_color", (0.9, 0.9, 1.0))
        )
    elif planet_type == PlanetType.GAS_GIANT:
        return generator.generate_gas_giant_texture(
            primary_color=config.get("primary_color", (0.8, 0.6, 0.4)),
            secondary_color=config.get("secondary_color", (0.9, 0.8, 0.6)),
            storm_color=config.get("storm_color", (0.9, 0.3, 0.2))
        )
    elif planet_type == PlanetType.ICE_GIANT:
        return generator.generate_ice_giant_texture(
            base_color=config.get("base_color", (0.3, 0.5, 0.7)),
            cloud_color=config.get("cloud_color", (0.6, 0.75, 0.9))
        )
    elif planet_type == PlanetType.ROCKY:
        return generator.generate_rocky_texture(
            base_color=config.get("base_color", (0.5, 0.4, 0.35)),
            crater_color=config.get("crater_color", (0.3, 0.25, 0.2))
        )
    else:
        # Fallback
        return generator.generate_rocky_texture()
