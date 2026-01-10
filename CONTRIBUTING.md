# Contributing to SolarSystem

Thank you for your interest in contributing to the SolarSystem project! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, Panda3D version)
- Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you might have

### Code Contributions

1. **Fork the repository** and create a new branch for your feature or fix
2. **Follow the coding style** used in the project:
   - PEP 8 style guidelines for Python code
   - Clear, descriptive variable and function names
   - Docstrings for classes and non-trivial functions
   - Comments for complex logic

3. **Test your changes** thoroughly:
   - Ensure the application runs without errors
   - Test all affected functionality
   - Verify no existing features are broken

4. **Document your changes**:
   - Update relevant docstrings
   - Update README.md if adding new features
   - Add comments for complex code

5. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots for visual changes

## Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SolarSystem
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python -m src.SolarSystem.Main
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8 conventions
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all classes and public methods

### Docstring Format
```python
def function_name(param1, param2):
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    pass
```

### Imports
- Group imports: standard library, third-party, local
- Use try/except for flexible imports (see existing code)

### Constants
- Add all configuration values to `constants.py`
- Use UPPER_CASE for constant names
- Group related constants with comments

## Project Structure

When adding new features:
- Place new modules in `src/SolarSystem/`
- Add configuration to `constants.py`
- Update `Main.py` if new subsystem initialization is needed
- Keep separation of concerns (each module has one responsibility)

## Adding New Celestial Bodies

To add a new planet or moon:

1. Add texture file to `models/` directory
2. Add planet data to `PLANETS` list in `constants.py`:
   ```python
   {
       "name": "planet_name",
       "orbit_au": 1.0,
       "size_scale": 1.0,
       "year_factor": 1.0,
       "day_factor": 1.0,
       "texture": "texture_file.jpg",
       "has_orbit": True,
   }
   ```
3. For moons, add `"parent": "planet_name"` to the configuration
4. Update `DEFAULT_TEXTURES` dictionary if needed
5. Test the new celestial body thoroughly

## Commit Messages

Use clear, descriptive commit messages:
- Start with a verb in present tense (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed after a blank line

Examples:
```
Add Saturn with rings and moons
Fix moon orbit calculation bug
Update camera controls for better usability
```

## Testing

Before submitting a pull request:
- [ ] Application starts without errors
- [ ] All existing features still work
- [ ] New features work as expected
- [ ] No console errors or warnings
- [ ] Code follows style guidelines
- [ ] Documentation is updated

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainer (Fock)

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to SolarSystem! 🌍🚀
