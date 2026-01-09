"""
ActionHandler module for SolarSystem application.
Handles all user input and UI interactions.
"""

from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode
from direct.gui.DirectGui import OnscreenText
import sys

try:
    from .constants import (
        MODELS_PATH, DEFAULT_TEXTURES, EASTER_EGG_TEXTURES,
        UI_TEXT_SCALE, UI_TITLE_SCALE, UI_TEXT_COLOR, PLANET_NAMES
    )
except ImportError:
    from constants import (
        MODELS_PATH, DEFAULT_TEXTURES, EASTER_EGG_TEXTURES,
        UI_TEXT_SCALE, UI_TITLE_SCALE, UI_TEXT_COLOR, PLANET_NAMES
    )


class ActionHandler(DirectObject):
    """
    Handles user input and controls for the solar system simulation.

    Manages keyboard events for:
    - Pausing/resuming simulation
    - Speed control
    - Texture toggling
    - Planet visibility
    """

    # Animation keys for each planet (Day rotation, Orbit rotation)
    PLANET_ANIMATIONS = {
        "sun": ["sunDay"],
        "mercury": ["mercuryDay", "mercuryOrbit"],
        "venus": ["venusDay", "venusOrbit"],
        "earth": ["earthDay", "earthOrbit"],
        "moon": ["moonDay", "moonOrbit"],
        "mars": ["marsDay", "marsOrbit"],
        "jupiter": ["jupiterDay", "jupiterOrbit"],
    }

    def __init__(self, base, cbAttDic, cbAttTex):
        """
        Initialize the ActionHandler.

        Args:
            base: Panda3D ShowBase instance
            cbAttDic: Dictionary of celestial body animation intervals
            cbAttTex: Dictionary of celestial body textures and models
        """
        DirectObject.__init__(self)
        self.base = base
        self.cbAttDic = cbAttDic
        self.cbAttTex = cbAttTex

        # State variables
        self.simRunning = True
        self.instructionsVisible = True
        self.usingOriginalTextures = True

        # UI text elements
        self._init_ui_elements()

    def _init_ui_elements(self):
        """Initialize UI text element references to None."""
        self.instructionText = None
        self.spaceKeyEventText = None
        self.speedUpText = None
        self.slowDownText = None
        self.toggleTextureText = None
        self.resetSolarSystemText = None
        self.easterEggText = None
        self.speedText = None
        self.title = None

    def _gen_label_text(self, text, line_number):
        """
        Generate a label text at the specified line position.

        Args:
            text: The text to display
            line_number: Line number (vertical position)

        Returns:
            OnscreenText instance
        """
        return OnscreenText(
            text=text,
            pos=(0.06, -0.06 * (line_number + 0.5)),
            fg=UI_TEXT_COLOR,
            parent=base.a2dTopLeft,
            align=TextNode.ALeft,
            scale=UI_TEXT_SCALE
        )

    def initAll(self):
        """Initialize all UI elements and activate key bindings."""
        self._display_title()
        self._display_instructions()
        self._activate_key_bindings()

    def _display_title(self):
        """Display the application title."""
        self.title = OnscreenText(
            text="Fock & Polydor - SolarSystem",
            parent=base.a2dBottomRight,
            align=TextNode.ARight,
            style=1,
            fg=UI_TEXT_COLOR,
            pos=(-0.1, 0.1),
            scale=UI_TITLE_SCALE
        )

    def _display_instructions(self):
        """Display all instruction text elements."""
        self.instructionText = self._gen_label_text("[I]: Hide Instructions", 1)
        self.speedText = self._gen_label_text("Speed x 1", 2)
        self.speedUpText = self._gen_label_text("[+]: SPEED UP!", 3)
        self.slowDownText = self._gen_label_text("[-]: slow down...", 4)
        self.toggleTextureText = self._gen_label_text("[T]: Toggle Texture", 5)
        self.resetSolarSystemText = self._gen_label_text("[R]: Reset Solar System", 6)
        self.easterEggText = self._gen_label_text("[X, Y, C, B, V]: Something Special", 7)
        self.spaceKeyEventText = self._gen_label_text("[SPACE]: Toggle entire Solar System", 8)

    def _show_instructions(self):
        """Show all instruction text."""
        self.instructionText.setText("[I]: Hide Instructions")
        self.spaceKeyEventText.setText("[SPACE]: Toggle entire Solar System")
        self.speedUpText.setText("[+]: SPEED UP!")
        self.slowDownText.setText("[-]: slow down...")
        self.toggleTextureText.setText("[T]: Toggle Texture")
        self.resetSolarSystemText.setText("[R]: Reset Solar System")
        self.easterEggText.setText("[X, Y, C, B, V]: Something Special")

    def _hide_instructions(self):
        """Hide all instruction text except the toggle hint."""
        self.spaceKeyEventText.setText("")
        self.speedUpText.setText("")
        self.slowDownText.setText("")
        self.toggleTextureText.setText("")
        self.resetSolarSystemText.setText("")
        self.easterEggText.setText("")
        self.instructionText.setText("[I]: Show Instructions")

    def _activate_key_bindings(self):
        """Set up all keyboard event handlers."""
        self.accept("escape", sys.exit)
        self.accept("e", self._handle_earth)
        self.accept("space", self._handle_all)
        self.accept("+", self._speed_up)
        self.accept("-", self._slow_down)
        self.accept("t", self._toggle_texture)
        self.accept("i", self._toggle_instructions)
        self.accept("r", self._reset_solar_system)
        self.accept("z", self._unlimit)
        self.accept("b", lambda: self._load_easter_egg_texture("borko"))
        self.accept("x", lambda: self._load_easter_egg_texture("team"))
        self.accept("y", lambda: self._load_easter_egg_texture("marm"))
        self.accept("c", lambda: self._load_easter_egg_texture("brezina"))
        self.accept("v", lambda: self._load_easter_egg_texture("testbild"))

    def _toggle_instructions(self):
        """Toggle visibility of instruction text."""
        if self.instructionsVisible:
            self._hide_instructions()
            self.instructionsVisible = False
        else:
            self._show_instructions()
            self.instructionsVisible = True

    def _set_all_play_rates(self, rate):
        """
        Set play rate for all animation intervals.

        Args:
            rate: The play rate to set (1.0 = normal, 0 = stopped, negative = reverse)
        """
        for planet, anim_keys in self.PLANET_ANIMATIONS.items():
            for key in anim_keys:
                if key in self.cbAttDic:
                    self.cbAttDic[key].setPlayRate(rate)

    def _adjust_all_play_rates(self, delta):
        """
        Adjust play rate for all animation intervals by a delta value.

        Args:
            delta: Amount to add to current play rate (positive or negative)
        """
        for planet, anim_keys in self.PLANET_ANIMATIONS.items():
            for key in anim_keys:
                if key in self.cbAttDic:
                    current_rate = self.cbAttDic[key].getPlayRate()
                    self.cbAttDic[key].setPlayRate(current_rate + delta)

    def _get_current_speed(self):
        """Get the current simulation speed from sun's day rotation."""
        return self.cbAttDic["sunDay"].getPlayRate()

    def _update_speed_display(self):
        """Update the speed display text."""
        speed = self._get_current_speed()
        self.speedText.setText(f"Speed x {speed}")

    def _speed_up(self):
        """Increase simulation speed."""
        current_speed = self._get_current_speed()

        # If at -1 (reversing slowly), jump to 1 (normal speed)
        if current_speed == -1:
            self._set_all_play_rates(1)
        else:
            self._adjust_all_play_rates(1)

        self._update_speed_display()

    def _slow_down(self):
        """Decrease simulation speed."""
        current_speed = self._get_current_speed()

        # If at 1 (normal speed), jump to -1 (reverse)
        if current_speed == 1:
            self._set_all_play_rates(-1)
        else:
            self._adjust_all_play_rates(-1)

        self._update_speed_display()

    def _unlimit(self):
        """Dramatically increase Earth and Moon speed (hidden feature)."""
        earth_moon_keys = ["earthOrbit", "earthDay", "moonOrbit", "moonDay"]
        for key in earth_moon_keys:
            if key in self.cbAttDic:
                current_rate = self.cbAttDic[key].getPlayRate()
                self.cbAttDic[key].setPlayRate(current_rate + 100)

    def _reset_solar_system(self):
        """Reset simulation to stopped state."""
        self._set_all_play_rates(0)
        self._update_speed_display()

    def _handle_earth(self):
        """Toggle Earth and Moon animation."""
        self._toggle_planet("earth", ["earthDay", "earthOrbit"])
        self._toggle_planet("moon", ["moonDay", "moonOrbit"])

    def _handle_all(self):
        """Toggle all planets' animation (pause/resume entire simulation)."""
        if self.simRunning:
            # Pause all running animations
            for planet, anim_keys in self.PLANET_ANIMATIONS.items():
                day_key = anim_keys[0]  # Day rotation is always first
                if day_key in self.cbAttDic and self.cbAttDic[day_key].isPlaying():
                    self._toggle_planet(planet, anim_keys)
        else:
            # Resume all paused animations
            for planet, anim_keys in self.PLANET_ANIMATIONS.items():
                day_key = anim_keys[0]
                if day_key in self.cbAttDic and not self.cbAttDic[day_key].isPlaying():
                    self._toggle_planet(planet, anim_keys)

        self.simRunning = not self.simRunning

    def _toggle_planet(self, planet_name, anim_keys):
        """
        Toggle animation for a specific planet.

        Args:
            planet_name: Name of the planet
            anim_keys: List of animation keys to toggle
        """
        for key in anim_keys:
            if key in self.cbAttDic:
                self._toggle_interval(self.cbAttDic[key])

    def _toggle_interval(self, interval):
        """
        Toggle an animation interval between playing and paused.

        Args:
            interval: The Panda3D interval to toggle
        """
        if interval.isPlaying():
            interval.pause()
        else:
            interval.resume()

    def _toggle_texture(self):
        """Toggle between original and alternate (white) textures."""
        if self.usingOriginalTextures:
            self._load_texture_for_all("weiss")
            self.usingOriginalTextures = False
        else:
            self._restore_original_textures()
            self.usingOriginalTextures = True

    def _load_easter_egg_texture(self, texture_name):
        """
        Load an easter egg texture for all planets.

        Args:
            texture_name: Name of the easter egg texture (without extension)
        """
        self.usingOriginalTextures = False
        self._load_texture_for_all(texture_name)

    def _load_texture_for_all(self, texture_name):
        """
        Load the same texture for all celestial bodies.

        Args:
            texture_name: Name of the texture file (without .jpg extension)
        """
        texture_path = f"{MODELS_PATH}{texture_name}.jpg"

        for planet in PLANET_NAMES:
            tex_key = f"{planet}Tex"
            if planet in self.cbAttTex:
                try:
                    new_tex = loader.loadTexture(texture_path)
                    self.cbAttTex[tex_key] = new_tex
                    self.cbAttTex[planet].setTexture(new_tex, 1)
                except Exception as e:
                    print(f"Warning: Could not load texture {texture_path}: {e}")

    def _restore_original_textures(self):
        """Restore the original textures for all celestial bodies."""
        for planet, texture_file in DEFAULT_TEXTURES.items():
            tex_key = f"{planet}Tex"
            texture_path = f"{MODELS_PATH}{texture_file}"

            if planet in self.cbAttTex:
                try:
                    new_tex = loader.loadTexture(texture_path)
                    self.cbAttTex[tex_key] = new_tex
                    self.cbAttTex[planet].setTexture(new_tex, 1)
                except Exception as e:
                    print(f"Warning: Could not load texture {texture_path}: {e}")


# Backwards compatibility aliases
ActionHandler.genLabelText = ActionHandler._gen_label_text
ActionHandler.displayLayout = ActionHandler._display_title
ActionHandler.displayLayoutAction = ActionHandler._display_instructions
ActionHandler.showLayoutAction = ActionHandler._show_instructions
ActionHandler.hideLayoutAction = ActionHandler._hide_instructions
ActionHandler.activateAction = ActionHandler._activate_key_bindings
ActionHandler.speedUp = ActionHandler._speed_up
ActionHandler.slowDown = ActionHandler._slow_down
ActionHandler.handleEarth = ActionHandler._handle_earth
ActionHandler.handleAll = ActionHandler._handle_all
ActionHandler.togglePlanet = ActionHandler._toggle_planet
ActionHandler.toggleInterval = ActionHandler._toggle_interval
ActionHandler.toggleTex = ActionHandler._toggle_texture
ActionHandler.loadTex = ActionHandler._load_texture_for_all
ActionHandler.resumeToNormalTex = ActionHandler._restore_original_textures
ActionHandler.resetSolarSystem = ActionHandler._reset_solar_system
ActionHandler.toggleInstructions = ActionHandler._toggle_instructions
