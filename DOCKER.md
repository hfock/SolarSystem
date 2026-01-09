# Docker Setup for SolarSystem

This document explains how to run the SolarSystem application using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)
- X11 server (for GUI display)

## Quick Start

### On Linux

1. Allow Docker to connect to X server:
   ```bash
   xhost +local:docker
   ```

2. Build and run the application:
   ```bash
   docker-compose up --build
   ```

3. To stop the application:
   ```bash
   docker-compose down
   ```

4. Restore X server security after use:
   ```bash
   xhost -local:docker
   ```

### On macOS

1. Install and start XQuartz:
   ```bash
   brew install --cask xquartz
   open -a XQuartz
   ```

2. In XQuartz preferences (XQuartz → Preferences → Security):
   - Enable "Allow connections from network clients"

3. Allow connections and set DISPLAY variable:
   ```bash
   xhost +localhost
   export DISPLAY=:0
   ```

4. Build and run:
   ```bash
   docker-compose up --build
   ```

### On Windows

1. Install and run VcXsrv or Xming X server

2. Set DISPLAY environment variable:
   ```powershell
   $env:DISPLAY="host.docker.internal:0"
   ```

3. Build and run:
   ```bash
   docker-compose up --build
   ```

## Building the Docker Image

To build the Docker image manually:

```bash
docker build -t solarsystem:latest .
```

## Running the Container

### Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Using Docker CLI

```bash
# Run the application
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  solarsystem:latest

# Run with custom parameters
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/src:/app/src \
  --network host \
  solarsystem:latest
```

## Development Mode

The docker-compose.yml file includes volume mounts for development:

- `./src:/app/src` - Maps source code for live editing
- `./models:/app/models` - Maps model files

To use development mode:

1. Make changes to your local source files
2. Restart the container to see changes:
   ```bash
   docker-compose restart
   ```

## Troubleshooting

### "Cannot open display" error

**Solution:**
- Ensure X server is running
- Grant access: `xhost +local:docker` (Linux) or `xhost +localhost` (macOS)
- Verify DISPLAY variable: `echo $DISPLAY`

### Container starts but no window appears

**Solution:**
- Check if X server is running
- Verify X11 socket is mounted: `ls /tmp/.X11-unix`
- On macOS, ensure XQuartz is running

### "Permission denied" for X11 socket

**Solution:**
- Run `xhost +local:docker` before starting
- On Linux, check X11 socket permissions: `ls -la /tmp/.X11-unix`

### Application crashes immediately

**Solution:**
- Check logs: `docker-compose logs`
- Verify all model files are present in `models/` directory
- Ensure Panda3D dependencies are installed correctly

## Performance Considerations

- **GPU Acceleration**: This setup uses software rendering. For hardware acceleration, you may need additional Docker GPU support (nvidia-docker for NVIDIA GPUs).
- **Network Mode**: Uses `host` networking for better X11 performance. Change to `bridge` if network isolation is required.

## Security Notes

- `xhost +local:docker` allows Docker containers to access your X server
- Always run `xhost -local:docker` after use to restore security
- For production deployments, consider using more secure X11 forwarding methods

## Production Deployment

For production deployment without GUI:

1. Remove X11 dependencies from Dockerfile
2. Modify application to support headless mode or offscreen rendering
3. Use environment variables for configuration
4. Remove volume mounts for source code

## Additional Commands

```bash
# View running containers
docker ps

# Execute commands in running container
docker-compose exec solarsystem bash

# Remove all containers and images
docker-compose down --rmi all

# Rebuild without cache
docker-compose build --no-cache
```

## Environment Variables

Available environment variables:

- `DISPLAY` - X11 display to use (default: `:0`)
- `PYTHONPATH` - Python module search path (default: `/app`)

## File Structure in Container

```
/app/
├── src/
│   └── SolarSystem/
│       ├── Main.py
│       ├── Universe.py
│       ├── CelestialBody.py
│       └── ...
├── models/
│   ├── *.jpg
│   ├── *.egg.pz
│   └── *.ptf
└── requirements.txt
```

## Support

For issues with Docker setup, please check:
- Docker logs: `docker-compose logs`
- System logs: `journalctl -xe` (Linux)
- X server logs: Check XQuartz console (macOS) or Event Viewer (Windows)
