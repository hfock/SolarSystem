# Documentation

This directory contains project documentation and design files for the SolarSystem application.

## Files

### Project Documentation
- **Fock_Polydor_SolarSystem.pdf** - Complete project documentation in PDF format
- **Fock_Polydor_SolarSystem.docx** - Editable project documentation in Word format

### Design Files
- **SolarSystem.asta** - Astah UML design file (architecture diagrams)
- **SolarSystem.bmpr** - Balsamiq mockup file (UI/UX wireframes)

### Diagrams & Screenshots
- **SolarSystemUML.png** - UML class diagram of the application architecture
- **SolarSystem.png** - Application screenshot or overview diagram
- **SolarSystemAusschnitt.png** - Detailed view/screenshot of the application

## Architecture Overview

The SolarSystem application follows a modular design with clear separation of concerns:

1. **Main** - Application orchestration and initialization
2. **Universe** - Environment management (lighting, skybox)
3. **CelestialBody** - Planet and moon data and animation
4. **CameraHandler** - View management
5. **ActionHandler** - Input processing and UI
6. **SpecialClass** - Visual effects (particles)

For detailed information, please refer to the PDF documentation.

## Editing Documentation

To modify the documentation:
- Edit `Fock_Polydor_SolarSystem.docx` with Microsoft Word or compatible editor
- Export updated version as PDF to maintain consistency
- Update UML diagrams using Astah UML
- Update mockups using Balsamiq Mockups

## For Developers

When making significant code changes:
1. Update the main README.md in the project root
2. Update relevant sections in the documentation
3. Regenerate UML diagrams if architecture changes
4. Update screenshots if UI changes
