# Extending the Solar System - Developer Guide

## Overview

The Solar System architecture has been optimized for easy expandability. Adding new celestial bodies (planets, moons, asteroids) requires **only** modifying the `PLANETS` list in `constants.py` - everything else is handled automatically!

## Quick Start: Adding a New Planet

### Example: Adding Saturn

1. Open `src/SolarSystem/constants.py`
2. Add your planet to the `PLANETS` list:

```python
{
    "name": "saturn",
    "orbit_au": 9.54,          # Distance from sun in AU
    "size_scale": 1.5,         # Visual size (Earth = 1.0)
    "year_factor": 29.46,      # Orbital period (Earth years)
    "day_factor": 0.44,        # Rotation period (Earth days)
    "texture": "saturn_1k_tex.jpg",  # Texture file in models/
    "has_orbit": True,         # Does it orbit?
},
```

3. Place your texture file in `models/saturn_1k_tex.jpg`
4. Run the application - **that's it!**

The system automatically:
- ✅ Validates your configuration on startup
- ✅ Creates animation keys (`saturnDay`, `saturnOrbit`)
- ✅ Adds to planet registry
- ✅ Handles texture loading
- ✅ Integrates with UI controls

## Adding Moons

Moons are defined just like planets, but with a `parent` field:

```python
# First define the parent planet
{
    "name": "saturn",
    "orbit_au": 9.54,
    "size_scale": 1.5,
    "year_factor": 29.46,
    "day_factor": 0.44,
    "texture": "saturn_1k_tex.jpg",
    "has_orbit": True,
    "moons": ["titan", "enceladus"],  # Optional documentation
},

# Then define moons AFTER their parent
{
    "name": "titan",
    "orbit_au": 0.2,           # Relative to Saturn (not sun!)
    "size_scale": 0.4,
    "year_factor": 0.044,
    "day_factor": 0.044,       # Tidally locked
    "texture": "titan_1k_tex.jpg",
    "has_orbit": True,
    "parent": "saturn",        # REQUIRED for moons
},
{
    "name": "enceladus",
    "orbit_au": 0.15,
    "size_scale": 0.15,
    "year_factor": 0.0038,
    "day_factor": 0.0038,
    "texture": "enceladus_1k_tex.jpg",
    "has_orbit": True,
    "parent": "saturn",
},
```

**Important:** Moons must be defined AFTER their parent planet in the list.

## Field Reference

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Unique identifier (lowercase recommended) | `"saturn"` |
| `orbit_au` | float | Orbital distance in AU (or relative to parent for moons) | `9.54` |
| `size_scale` | float | Visual size multiplier (must be > 0) | `1.5` |
| `year_factor` | float | Orbital period in Earth years | `29.46` |
| `day_factor` | float | Rotation period in Earth days (or seconds for sun) | `0.44` |
| `texture` | string | Texture filename in `models/` directory | `"saturn_1k_tex.jpg"` |
| `has_orbit` | boolean | Whether this body orbits | `true` |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `parent` | string | Parent body name (for moons) | `"saturn"` |
| `moons` | list | List of moon names (documentation only) | `["titan"]` |
| `custom_*` | any | Custom properties for extensions | `"custom_has_rings": true` |

## Advanced Features

### Custom Properties

Add any property starting with `custom_` to enable future extensions:

```python
{
    "name": "saturn",
    "orbit_au": 9.54,
    "size_scale": 1.5,
    "year_factor": 29.46,
    "day_factor": 0.44,
    "texture": "saturn_1k_tex.jpg",
    "has_orbit": True,

    # Custom properties (automatically preserved)
    "custom_has_rings": True,
    "custom_ring_texture": "saturn_rings.png",
    "custom_atmosphere_color": [0.9, 0.8, 0.6],
    "custom_special_effect": "gas_giant",
},
```

Access custom properties in code:

```python
# In Planet class or extensions
planet = celestial_body.planets["saturn"]
if hasattr(planet, 'custom_has_rings') and planet.custom_has_rings:
    # Render rings
    render_rings(planet.custom_ring_texture)
```

### Multiple Moons

No limit on moons per planet:

```python
{
    "name": "jupiter",
    "orbit_au": 5.2,
    "size_scale": 2.0,
    # ... other fields
    "moons": ["io", "europa", "ganymede", "callisto"],  # Documentation
},
# Then define each moon with parent: "jupiter"
```

## Configuration Validation

The system validates configurations on startup and will exit with clear error messages:

```
CONFIGURATION ERROR: Planet 'saturn' missing required field 'texture'
CONFIGURATION ERROR: Planet 'titan' has parent 'saturn' which is not defined
CONFIGURATION ERROR: Duplicate planet name found: 'earth'
CONFIGURATION ERROR: Planet 'mars' has invalid size_scale: -0.5
```

## Architecture Benefits

### Before Optimization (Old Architecture)
To add a new planet, you had to:
1. ❌ Add to `PLANETS` list
2. ❌ Add to `PLANET_NAMES` list
3. ❌ Add to `DEFAULT_TEXTURES` dict
4. ❌ Add to `PLANET_ANIMATIONS` dict in ActionHandler
5. ❌ Create `loadPlanetName()` method
6. ❌ Create `rotatePlanetName()` method
7. ❌ Hope everything stayed in sync!

### After Optimization (New Architecture)
To add a new planet, you only need to:
1. ✅ Add to `PLANETS` list
2. ✅ Add texture file to `models/`

**That's it!** Everything else is automatic.

## Real-World Examples

### Adding Neptune with Triton

```python
# Add to PLANETS list in constants.py
{
    "name": "neptune",
    "orbit_au": 30.07,
    "size_scale": 3.88,
    "year_factor": 164.8,
    "day_factor": 0.67,
    "texture": "neptune_1k_tex.jpg",
    "has_orbit": True,
    "moons": ["triton"],
    "custom_color": [0.2, 0.3, 0.8],  # Blue color hint
},
{
    "name": "triton",
    "orbit_au": 0.23,
    "size_scale": 0.21,
    "year_factor": 0.016,
    "day_factor": 0.016,
    "texture": "triton_1k_tex.jpg",
    "has_orbit": True,
    "parent": "neptune",
    "custom_retrograde": True,  # Triton orbits backwards!
},
```

### Adding an Asteroid Belt

```python
{
    "name": "ceres",
    "orbit_au": 2.77,
    "size_scale": 0.074,
    "year_factor": 4.6,
    "day_factor": 0.38,
    "texture": "ceres_1k_tex.jpg",
    "has_orbit": True,
    "custom_is_dwarf_planet": True,
},
```

### Adding a Comet

```python
{
    "name": "halley",
    "orbit_au": 17.8,      # Average distance
    "size_scale": 0.01,
    "year_factor": 75.3,   # 75 year orbit!
    "day_factor": 2.2,
    "texture": "comet_1k_tex.jpg",
    "has_orbit": True,
    "custom_has_tail": True,
    "custom_orbit_eccentricity": 0.967,  # Highly elliptical
},
```

## Testing Your Changes

After adding new bodies:

1. **Validation check** - The system validates on startup:
   ```bash
   cd src/SolarSystem
   python Main.py
   ```

2. **Check the logs** - Successful load:
   ```
   Loading solar system...
   Loaded planet: saturn
   Loaded moon: titan (parent: saturn)
   All celestial bodies loaded successfully!
   ```

3. **UI Controls** - Your new bodies automatically work with:
   - `SPACE` - Toggle all animations
   - `+/-` - Speed control
   - `T` - Texture toggle
   - `R` - Reset

## Best Practices

1. **Naming Convention**
   - Use lowercase names: `"saturn"` not `"Saturn"`
   - No spaces: `"io"` not `"Io Moon"`
   - Keep names short and unique

2. **Order Matters**
   - Define parent planets before their moons
   - Generally order by distance from sun (not required, but cleaner)

3. **Texture Preparation**
   - Use 1K-2K resolution JPGs for best performance
   - Name pattern: `{name}_1k_tex.jpg`
   - Equirectangular projection for planets

4. **Scale Considerations**
   - `size_scale`: Visual size (not realistic, optimized for visibility)
   - `orbit_au`: Can be compressed for inner planets to fit screen
   - Balance realism with visual appeal

5. **Documentation**
   - Use comments to explain unusual values
   - Use `moons` field to document moon relationships
   - Use `custom_*` for future-proofing

## Troubleshooting

### Error: "Planet X missing required field Y"
- Check all required fields are present
- Common mistake: forgetting `has_orbit`

### Error: "Parent planet Y not found for moon X"
- Ensure parent planet is defined BEFORE the moon in PLANETS list
- Check spelling of parent name

### Error: "Duplicate planet name found: X"
- Each `name` must be unique
- Search PLANETS list for duplicate entries

### Texture not loading
- Check file exists in `models/` directory
- Verify file extension matches (.jpg, .png, .jpeg)
- Check file permissions

### Moon not orbiting correctly
- `orbit_au` for moons is relative to parent, not sun
- Check `parent` field matches parent planet name exactly

## Future Extension Ideas

With custom properties, you can extend the system:

1. **Planetary Rings**
   ```python
   "custom_has_rings": True,
   "custom_ring_inner": 1.2,
   "custom_ring_outer": 2.3,
   ```

2. **Atmospheric Effects**
   ```python
   "custom_atmosphere": True,
   "custom_atmosphere_color": [0.5, 0.8, 1.0],
   "custom_atmosphere_density": 0.3,
   ```

3. **Special Lighting**
   ```python
   "custom_emissive": True,
   "custom_light_color": [1.0, 0.9, 0.7],
   "custom_light_intensity": 2.5,
   ```

4. **Orbital Mechanics**
   ```python
   "custom_eccentricity": 0.2,
   "custom_inclination": 7.0,
   "custom_retrograde": True,
   ```

Then modify the `Planet` class to use these properties!

## Summary

The optimized architecture makes the Solar System **truly expandable**:

- **Single Source of Truth**: Only edit `PLANETS` list
- **Auto-validation**: Catch errors immediately
- **Zero Boilerplate**: No duplicate code needed
- **Future-proof**: Custom properties for extensions
- **Clean Code**: 97 lines of legacy code removed

Ready to supercharge your solar system? Just add to the `PLANETS` list and watch the magic happen! ✨
