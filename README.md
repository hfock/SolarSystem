# SolarSystem

A 3D interactive solar system simulator built with Panda3D.

**Authors:** Fock

## Overview

SolarSystem is an educational and interactive 3D visualization of our solar system. It features realistic planetary orbits, rotation periods, particle effects, and an intuitive control interface. The simulation is built using the Panda3D game engine and provides an engaging way to explore celestial mechanics.

## Features

- **Realistic Celestial Bodies**: Sun, Mercury, Venus, Earth, Moon, Mars, and Jupiter
- **Accurate Orbital Mechanics**: Planets orbit at scaled distances and periods
- **Day/Night Cycles**: Each celestial body rotates on its axis with realistic timing
- **Particle Effects**: Dynamic fire-like particle effects on the sun
- **Interactive Camera**: Mouse-controlled trackball camera for 360° viewing
- **Speed Control**: Speed up, slow down, or reverse time
- **Texture Toggle**: Switch between different texture sets
- **Easter Eggs**: Hidden special textures for fun exploration

## Requirements

- Python 3.6 or higher
- Panda3D 1.10.0 or higher

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd SolarSystem
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `models/` directory contains all required assets:
   - Planet model (`planet_sphere`)
   - Skybox model (`solar_sky_sphere`)
   - Planet textures (`.jpg` files)
   - Particle effect configuration (`fireish.ptf`)

## Docker Installation (Alternative)

The application can also be run using Docker, which simplifies dependency management and ensures consistent environments across different systems.

### Prerequisites

- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)
- X11 server for GUI display (on Linux, usually pre-installed)

### Running with Docker Compose (Recommended)

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd SolarSystem
   ```

2. Allow Docker to access your display (Linux only):
   ```bash
   xhost +local:docker
   ```

3. Start the application:
   ```bash
   docker-compose up
   ```

4. To stop the application, press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

### Running with Docker (Without Compose)

1. Build the Docker image:
   ```bash
   docker build -t solarsystem .
   ```

2. Allow Docker to access your display (Linux only):
   ```bash
   xhost +local:docker
   ```

3. Run the container:
   ```bash
   docker run --rm -it \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     --network host \
     solarsystem
   ```

### Docker on macOS/Windows

For macOS and Windows users, you'll need to set up an X11 server:

**macOS:**
1. Install XQuartz: `brew install --cask xquartz`
2. Start XQuartz application (via Spotlight or Applications folder)
3. In XQuartz Preferences → Security, enable "Allow connections from network clients"
4. Restart XQuartz for the changes to take effect
5. Open a terminal and allow X11 connections:
   ```bash
   xhost +
   ```
   **Note:** If `xhost` shows "unable to open display", XQuartz is not running yet. Make sure you see the XQuartz icon in your menu bar.

6. Start the application using the macOS-specific compose file:
   ```bash
   docker-compose -f docker-compose.mac.yml up
   ```

   Alternatively, set DISPLAY manually with the regular compose file:
   ```bash
   DISPLAY=host.docker.internal:0 docker-compose up
   ```

**Windows:**
1. Install VcXsrv or Xming
2. Start the X server with "Disable access control" enabled
3. Set DISPLAY in docker-compose.yml to your Windows IP address

### Troubleshooting Docker

- **Black screen or no display**: Ensure `xhost +local:docker` was run before starting
- **Permission denied errors**: Check X11 socket permissions in `/tmp/.X11-unix`
- **Application crashes on startup**: Verify all model files are present in the `models/` directory

## Usage

Run the application from the project root:

```bash
python -m src.SolarSystem.Main
```

Or directly:

```bash
python src/SolarSystem/Main.py
```

## Controls

### Basic Controls
- **SPACE**: Pause/Resume entire simulation
- **ESC**: Exit application
- **I**: Toggle instruction visibility

### Speed Control
- **+**: Speed up simulation
- **-**: Slow down simulation (or reverse time)
- **R**: Reset simulation (stop all motion)
- **Z**: Unlock Earth and Moon speed (hidden feature)

### Display Options
- **T**: Toggle between original and alternate textures
- **E**: Toggle Earth and Moon animation

### Easter Eggs
- **X**: Team texture
- **Y**: Marm texture
- **C**: Brezina texture
- **B**: Borko texture
- **V**: Test pattern texture

### Camera
- **Mouse**: Drag to rotate camera view using trackball controls

## Project Structure

```
SolarSystem/
├── src/
│   └── SolarSystem/
│       ├── Main.py              # Application entry point
│       ├── Universe.py          # Environment setup (lighting, skybox)
│       ├── CelestialBody.py     # Planet and moon management
│       ├── CameraHandler.py     # Camera positioning
│       ├── ActionHandler.py     # User input and UI
│       ├── SpecialClass.py      # Particle effects
│       ├── constants.py         # Configuration constants
│       └── __init__.py
├── models/                      # 3D models and textures
│   ├── *.jpg                    # Planet texture files
│   ├── *.egg.pz                 # Panda3D model files
│   └── fireish.ptf              # Particle effect configuration
├── docs/                        # Project documentation
│   ├── README.md                # Documentation overview
│   ├── *.pdf, *.docx            # Project documentation
│   └── *.png                    # Diagrams and screenshots
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
└── .gitignore                   # Git ignore rules
```

## Technical Details

### Architecture

The application follows a modular architecture with clear separation of concerns:

- **Main**: Initializes and orchestrates all subsystems
- **Universe**: Manages environmental elements (lighting, skybox)
- **CelestialBody**: Handles planet/moon loading, positioning, and animation
- **CameraHandler**: Sets up the viewing perspective
- **ActionHandler**: Processes user input and manages UI
- **SpecialClass**: Adds visual effects to celestial bodies

### Configuration

All simulation parameters are centralized in `constants.py`:
- `SIZE_SCALE`: Planet size multiplier (default: 0.6)
- `ORBIT_SCALE`: Orbital distance multiplier (default: 10)
- `YEAR_SCALE`: Year duration in seconds (default: 60)
- `DAY_SCALE`: Day duration scaling factor

### Planetary Data

Each planet is defined with realistic parameters:
- **Orbital distance** (in Astronomical Units)
- **Size scale** (relative to Earth)
- **Year factor** (orbital period relative to Earth)
- **Day factor** (rotation period in Earth days)

## Customization

### Adding New Planets

To add a new celestial body, edit `constants.py`:

```python
PLANETS = [
    # ... existing planets ...
    {
        "name": "saturn",
        "orbit_au": 9.54,
        "size_scale": 9.45,
        "year_factor": 29.46,
        "day_factor": 0.44,
        "texture": "saturn_texture.jpg",
        "has_orbit": True,
    },
]
```

### Adjusting Simulation Speed

Modify the scale constants in `constants.py`:

```python
YEAR_SCALE = 120  # Make years take 2 minutes instead of 1
DAY_SCALE = YEAR_SCALE / 365.0 * 5
```

## Known Limitations

- Only includes major planets up to Jupiter (outer planets Saturn, Uranus, Neptune not included)
- Orbits are circular (not elliptical as in reality)
- Planet sizes and distances are scaled differently for visibility
- Moons are simplified (only Earth's Moon is included)

## Future Enhancements

- Add remaining planets (Saturn, Uranus, Neptune)
- Implement elliptical orbits
- Add more moons for gas giants
- Include asteroid belt visualization
- Add planet information panels
- Implement trajectory prediction lines

## Documentation

For detailed project documentation, design diagrams, and architecture information, please see the [docs/](docs/) directory:
- **Complete Documentation**: `docs/Fock_Polydor_SolarSystem.pdf`
- **UML Diagrams**: `docs/SolarSystemUML.png`
- **Screenshots**: `docs/SolarSystem.png`

## Credits

- **Panda3D**: The 3D rendering engine
- **Textures**: Various sources for planetary textures
- **Particle Effects**: Custom fire effect configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

**Fock & Polydor - SolarSystem**
An educational 3D solar system simulator
