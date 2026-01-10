"""
Enhanced Materials and Shader System for Solar System
Provides advanced visual effects including atmosphere, specular highlights, and improved lighting.
"""

from panda3d.core import (
    Shader, Material, TextureStage, Texture, PNMImage,
    TransparencyAttrib, LVector3, LColor, NodePath
)
import numpy as np


class PlanetMaterial:
    """Enhanced material system for planets with advanced visual effects"""

    def __init__(self, model, planet_name):
        self.model = model
        self.planet_name = planet_name
        self.material = Material()

    def apply_basic_material(self, has_atmosphere=False, shininess=1.0,
                            specular=(0.3, 0.3, 0.3, 1.0), emission=(0, 0, 0, 1)):
        """Apply basic material properties to a planet"""
        self.material.setShininess(shininess)
        self.material.setSpecular(LColor(*specular))
        self.material.setEmission(LColor(*emission))

        if has_atmosphere:
            # More diffuse for atmospheric planets
            self.material.setDiffuse(LColor(1.0, 1.0, 1.0, 1.0))
            self.material.setAmbient(LColor(0.3, 0.3, 0.3, 1.0))
        else:
            # Less ambient for airless bodies
            self.material.setDiffuse(LColor(0.9, 0.9, 0.9, 1.0))
            self.material.setAmbient(LColor(0.2, 0.2, 0.2, 1.0))

        self.model.setMaterial(self.material)

    def create_atmosphere_shell(self, base, radius_scale=1.05, color=(0.3, 0.5, 0.8, 0.3)):
        """Create an atmospheric glow shell around the planet"""
        from panda3d.core import CardMaker, GeomNode

        # Create a slightly larger sphere for atmosphere
        atmosphere = loader.loadModel("models/planet_sphere")
        atmosphere.setScale(radius_scale)
        atmosphere.reparentTo(self.model)

        # Set up transparency
        atmosphere.setTransparency(TransparencyAttrib.MAlpha)

        # Create atmosphere material
        atmo_material = Material()
        atmo_material.setEmission(LColor(*color))
        atmo_material.setAmbient(LColor(0, 0, 0, 1))
        atmo_material.setDiffuse(LColor(*color))
        atmosphere.setMaterial(atmo_material)

        # Make it glow
        atmosphere.setColorScale(color[0], color[1], color[2], color[3])

        return atmosphere


class ShaderManager:
    """Manages custom shaders for enhanced visual effects"""

    VERTEX_SHADER = """
    #version 150

    uniform mat4 p3d_ModelViewProjectionMatrix;
    uniform mat4 p3d_ModelViewMatrix;
    uniform mat3 p3d_NormalMatrix;
    uniform mat4 p3d_ModelMatrix;

    in vec4 p3d_Vertex;
    in vec3 p3d_Normal;
    in vec2 p3d_MultiTexCoord0;

    out vec2 texcoord;
    out vec3 normal;
    out vec3 viewDir;
    out vec3 worldPos;

    void main() {
        gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
        texcoord = p3d_MultiTexCoord0;
        normal = normalize(p3d_NormalMatrix * p3d_Normal);

        vec4 viewPos = p3d_ModelViewMatrix * p3d_Vertex;
        viewDir = normalize(-viewPos.xyz);

        worldPos = (p3d_ModelMatrix * p3d_Vertex).xyz;
    }
    """

    FRAGMENT_SHADER_PLANET = """
    #version 150

    uniform sampler2D p3d_Texture0;
    uniform vec4 atmosphereColor;
    uniform float atmosphereIntensity;
    uniform float specularPower;
    uniform vec3 lightPos;

    in vec2 texcoord;
    in vec3 normal;
    in vec3 viewDir;
    in vec3 worldPos;

    out vec4 fragColor;

    void main() {
        // Base texture color
        vec4 texColor = texture(p3d_Texture0, texcoord);

        // Lighting calculations
        vec3 N = normalize(normal);
        vec3 L = normalize(lightPos - worldPos);
        vec3 V = normalize(viewDir);
        vec3 H = normalize(L + V);

        // Diffuse lighting
        float diffuse = max(dot(N, L), 0.0);

        // Specular highlight
        float specular = pow(max(dot(N, H), 0.0), specularPower);

        // Fresnel effect for atmosphere rim lighting
        float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.0);
        vec3 atmosphereGlow = atmosphereColor.rgb * fresnel * atmosphereIntensity;

        // Combine all lighting
        vec3 finalColor = texColor.rgb * (0.3 + diffuse * 0.7) +
                         specular * 0.3 +
                         atmosphereGlow;

        fragColor = vec4(finalColor, texColor.a);
    }
    """

    FRAGMENT_SHADER_STAR = """
    #version 150

    uniform sampler2D p3d_Texture0;
    uniform float pulseIntensity;
    uniform float time;

    in vec2 texcoord;
    in vec3 normal;
    in vec3 viewDir;

    out vec4 fragColor;

    void main() {
        vec4 texColor = texture(p3d_Texture0, texcoord);

        // Pulsating glow effect
        float pulse = 1.0 + sin(time * 2.0) * pulseIntensity;

        // Brighten the star
        vec3 glowColor = texColor.rgb * pulse * 1.5;

        fragColor = vec4(glowColor, texColor.a);
    }
    """

    @staticmethod
    def apply_planet_shader(model, atmosphere_color=(0.3, 0.5, 0.8, 1.0),
                          atmosphere_intensity=0.4, specular_power=32.0,
                          light_pos=(0, 0, 0)):
        """Apply enhanced planet shader with atmosphere and specular effects"""
        shader = Shader.make(Shader.SL_GLSL,
                           vertex=ShaderManager.VERTEX_SHADER,
                           fragment=ShaderManager.FRAGMENT_SHADER_PLANET)

        model.setShader(shader)
        model.setShaderInput("atmosphereColor", LVector3(*atmosphere_color[:3]))
        model.setShaderInput("atmosphereIntensity", atmosphere_intensity)
        model.setShaderInput("specularPower", specular_power)
        model.setShaderInput("lightPos", LVector3(*light_pos))

    @staticmethod
    def apply_star_shader(model, pulse_intensity=0.1):
        """Apply glowing star shader with pulsating effect"""
        shader = Shader.make(Shader.SL_GLSL,
                           vertex=ShaderManager.VERTEX_SHADER,
                           fragment=ShaderManager.FRAGMENT_SHADER_STAR)

        model.setShader(shader)
        model.setShaderInput("pulseIntensity", pulse_intensity)
        model.setShaderInput("time", 0.0)  # Will be updated in task


class NormalMapGenerator:
    """Generate normal maps from heightmaps for enhanced surface detail"""

    @staticmethod
    def create_normal_map_from_noise(width, height, noise_func, strength=1.0):
        """
        Create a normal map from a noise function.

        Args:
            width, height: Texture dimensions
            noise_func: Function that takes (x, y) and returns height value
            strength: Normal map intensity

        Returns:
            Panda3D Texture with normal map
        """
        img = PNMImage(width, height)

        for y in range(height):
            for x in range(width):
                u = x / width
                v = y / height

                # Sample heightmap at current position and neighbors
                h_center = noise_func(u, v)
                h_right = noise_func((x + 1) / width, v)
                h_up = noise_func(u, (y + 1) / height)

                # Calculate gradients
                dx = (h_right - h_center) * strength
                dy = (h_up - h_center) * strength

                # Convert to normal vector
                normal_x = -dx
                normal_y = -dy
                normal_z = 1.0

                # Normalize
                length = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
                if length > 0:
                    normal_x /= length
                    normal_y /= length
                    normal_z /= length

                # Convert from [-1, 1] to [0, 1] range for storage
                r = (normal_x + 1.0) * 0.5
                g = (normal_y + 1.0) * 0.5
                b = (normal_z + 1.0) * 0.5

                img.setXel(x, y, r, g, b)

        # Convert to texture
        texture = Texture()
        texture.load(img)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)

        return texture


# Planet-specific material configurations
PLANET_MATERIAL_CONFIGS = {
    "sun": {
        "type": "star",
        "shininess": 128.0,
        "specular": (0, 0, 0, 1),
        "emission": (0.8, 0.7, 0.4, 1),
        "has_atmosphere": False,
        "pulse_intensity": 0.08
    },
    "mercury": {
        "type": "rocky",
        "shininess": 5.0,
        "specular": (0.1, 0.1, 0.1, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": False,
        "atmosphere_color": None
    },
    "venus": {
        "type": "terrestrial",
        "shininess": 20.0,
        "specular": (0.4, 0.4, 0.3, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.8, 0.7, 0.4, 0.25),
        "atmosphere_intensity": 0.5
    },
    "earth": {
        "type": "terrestrial",
        "shininess": 25.0,
        "specular": (0.5, 0.5, 0.6, 1),  # Water specular
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.3, 0.5, 0.8, 0.3),
        "atmosphere_intensity": 0.6
    },
    "moon": {
        "type": "rocky",
        "shininess": 3.0,
        "specular": (0.05, 0.05, 0.05, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": False,
        "atmosphere_color": None
    },
    "mars": {
        "type": "terrestrial",
        "shininess": 8.0,
        "specular": (0.2, 0.15, 0.1, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.8, 0.4, 0.2, 0.15),
        "atmosphere_intensity": 0.3
    },
    "jupiter": {
        "type": "gas_giant",
        "shininess": 15.0,
        "specular": (0.3, 0.3, 0.25, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.7, 0.5, 0.3, 0.2),
        "atmosphere_intensity": 0.4
    },
    "saturn": {
        "type": "gas_giant",
        "shininess": 12.0,
        "specular": (0.35, 0.3, 0.2, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.8, 0.7, 0.5, 0.2),
        "atmosphere_intensity": 0.35
    },
    "uranus": {
        "type": "ice_giant",
        "shininess": 18.0,
        "specular": (0.3, 0.4, 0.45, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.4, 0.6, 0.7, 0.25),
        "atmosphere_intensity": 0.4
    },
    "neptune": {
        "type": "ice_giant",
        "shininess": 20.0,
        "specular": (0.2, 0.3, 0.5, 1),
        "emission": (0, 0, 0, 1),
        "has_atmosphere": True,
        "atmosphere_color": (0.2, 0.3, 0.6, 0.3),
        "atmosphere_intensity": 0.45
    }
}


def apply_enhanced_material(model, planet_name, use_shader=True):
    """
    Apply enhanced materials and shaders to a planet model.

    Args:
        model: The planet's model NodePath
        planet_name: Name of the planet
        use_shader: Whether to use shader-based effects (default True)

    Returns:
        PlanetMaterial instance
    """
    planet_name_lower = planet_name.lower()

    # Get configuration or use defaults
    if planet_name_lower not in PLANET_MATERIAL_CONFIGS:
        config = {
            "type": "rocky",
            "shininess": 5.0,
            "specular": (0.1, 0.1, 0.1, 1),
            "emission": (0, 0, 0, 1),
            "has_atmosphere": False
        }
    else:
        config = PLANET_MATERIAL_CONFIGS[planet_name_lower]

    # Create and apply material
    planet_material = PlanetMaterial(model, planet_name)
    planet_material.apply_basic_material(
        has_atmosphere=config.get("has_atmosphere", False),
        shininess=config.get("shininess", 5.0),
        specular=config.get("specular", (0.3, 0.3, 0.3, 1)),
        emission=config.get("emission", (0, 0, 0, 1))
    )

    # Apply shaders if enabled
    if use_shader:
        if config.get("type") == "star":
            ShaderManager.apply_star_shader(
                model,
                pulse_intensity=config.get("pulse_intensity", 0.1)
            )
        elif config.get("has_atmosphere"):
            ShaderManager.apply_planet_shader(
                model,
                atmosphere_color=config.get("atmosphere_color", (0.3, 0.5, 0.8, 1.0)),
                atmosphere_intensity=config.get("atmosphere_intensity", 0.4),
                specular_power=config.get("shininess", 32.0),
                light_pos=(0, 0, 0)  # Sun at origin
            )

    return planet_material
