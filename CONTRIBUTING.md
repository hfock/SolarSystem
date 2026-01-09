# Beitragen zum SolarSystem-Projekt

Vielen Dank für Ihr Interesse, zum SolarSystem-Projekt beizutragen!

## Entwicklungsumgebung einrichten

### Voraussetzungen

- Python 3.7+
- Git
- Panda3D

### Setup

```bash
# Repository klonen
git clone <repository-url>
cd SolarSystem

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
cd src/SolarSystem
python Main.py
```

## Projektstruktur verstehen

```
src/SolarSystem/
├── constants.py      # ALLE Konfigurationswerte hier
├── Main.py           # Einstiegspunkt
├── CelestialBody.py  # Planet-Klasse und -Verwaltung
├── ActionHandler.py  # Benutzereingaben
├── Universe.py       # Umgebung (Licht, Skybox)
├── CameraHandler.py  # Kamera
└── SpecialClass.py   # Partikeleffekte
```

## Code-Richtlinien

### Python-Stil

- **Python 3** kompatibel
- **PEP 8** Namenskonventionen:
  - `snake_case` für Funktionen und Variablen
  - `PascalCase` für Klassen
  - `UPPER_CASE` für Konstanten
- **Docstrings** für alle öffentlichen Klassen und Methoden
- **f-Strings** für String-Formatierung

### Beispiel

```python
class MyClass:
    """
    Kurze Beschreibung der Klasse.

    Längere Beschreibung falls nötig.
    """

    def my_method(self, param):
        """
        Beschreibung der Methode.

        Args:
            param: Beschreibung des Parameters

        Returns:
            Beschreibung des Rückgabewerts
        """
        return f"Result: {param}"
```

### Konstanten

**Wichtig:** Alle Magic Numbers und Konfigurationswerte gehören in `constants.py`:

```python
# Schlecht
self.planet.setScale(0.6)

# Gut
from .constants import SIZE_SCALE
self.planet.setScale(SIZE_SCALE)
```

### Fehlerbehandlung

Asset-Laden sollte immer mit try/except umgeben sein:

```python
try:
    model = loader.loadModel(path)
except Exception as e:
    print(f"Error: Could not load model: {e}")
    sys.exit(1)
```

## Neue Features hinzufügen

### Neuen Planeten hinzufügen

1. Textur in `models/` ablegen (z.B. `saturn_tex.jpg`)

2. Planet in `constants.py` eintragen:
   ```python
   PLANETS = [
       # ... bestehende Planeten ...
       {
           "name": "saturn",
           "orbit_au": 2.5,
           "size_scale": 0.8,
           "year_factor": 5.0,
           "day_factor": 0.44,
           "texture": "saturn_tex.jpg",
           "has_orbit": True,
       },
   ]
   ```

3. In `PLANET_NAMES` und `DEFAULT_TEXTURES` aufnehmen

4. Fertig! Der Planet wird automatisch geladen.

### Neuen Mond hinzufügen

```python
{
    "name": "phobos",
    "orbit_au": 0.05,
    "size_scale": 0.02,
    "year_factor": 0.02,
    "day_factor": 0.02,
    "texture": "phobos_tex.jpg",
    "has_orbit": True,
    "parent": "mars",  # Wichtig: Parent-Planet angeben
},
```

### Neue Tastenkombination hinzufügen

1. In `ActionHandler._activate_key_bindings()`:
   ```python
   self.accept("n", self._my_new_action)
   ```

2. Neue Methode implementieren:
   ```python
   def _my_new_action(self):
       """Beschreibung der Aktion."""
       # Implementation
   ```

## Tests

Aktuell gibt es keine automatisierten Tests. Bitte testen Sie Änderungen manuell:

1. Anwendung starten
2. Alle Tasten testen
3. Kamerasteuerung prüfen
4. Geschwindigkeitsänderungen testen
5. Texturwechsel prüfen

## Pull Requests

1. Fork erstellen
2. Feature-Branch anlegen (`git checkout -b feature/mein-feature`)
3. Änderungen committen (`git commit -m 'Add: Mein neues Feature'`)
4. Branch pushen (`git push origin feature/mein-feature`)
5. Pull Request erstellen

### Commit-Nachrichten

Format: `<type>: <beschreibung>`

Typen:
- `add`: Neues Feature
- `fix`: Bugfix
- `refactor`: Code-Refactoring
- `docs`: Dokumentation
- `style`: Formatierung

Beispiele:
```
add: Saturn als neuen Planeten hinzugefügt
fix: Texturwechsel funktioniert jetzt korrekt
refactor: ActionHandler Code-Duplizierung entfernt
docs: README mit Installationsanleitung erweitert
```

## Fragen?

Bei Fragen wenden Sie sich an die Autoren: **Fock & Polydor**
