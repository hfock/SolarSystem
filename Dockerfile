# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Panda3D and OpenGL
# Includes Mesa for software rendering (needed for macOS XQuartz compatibility)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglu1-mesa \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxrandr2 \
    libxcursor1 \
    libxinerama1 \
    libxxf86vm1 \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libosmesa6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Copy models and assets
COPY models/ ./models/

# Set PYTHONPATH to include src directory
ENV PYTHONPATH=/app

# Set display environment variable (will be overridden by docker-compose)
ENV DISPLAY=:0

# Force Mesa to use software rendering (llvmpipe) for compatibility with XQuartz
# This ensures OpenGL works even when hardware GLX is not available
ENV LIBGL_ALWAYS_SOFTWARE=1

# Run the application
CMD ["python", "-m", "src.SolarSystem.Main"]
