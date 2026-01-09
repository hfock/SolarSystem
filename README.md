# SolarSystem

Eine interaktive 3D-Simulation des Sonnensystems, entwickelt mit Python und dem Panda3D-Framework.

![SolarSystem Screenshot](docs/SolarSystemAusschnitt.png)

## Features

- Realistische Darstellung von Sonne, Merkur, Venus, Erde, Mond, Mars und Jupiter
- Interaktive Kamerasteuerung mit Maus
- Geschwindigkeitskontrolle der Simulation
- Wechselbare Planetentexturen
- Partikeleffekte für die Sonne
- Pause/Fortsetzen der gesamten Simulation

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- Panda3D Game Engine

### Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

Oder manuell:

```bash
pip install panda3d
```

## Verwendung

### Starten der Anwendung

```bash
cd src/SolarSystem
python Main.py
```

Oder als Python-Modul:

```bash
cd src
python -m SolarSystem.Main
```

### Tastatursteuerung

| Taste | Aktion |
|-------|--------|
| `SPACE` | Simulation pausieren/fortsetzen |
| `+` | Geschwindigkeit erhöhen |
| `-` | Geschwindigkeit verringern |
| `R` | Simulation zurücksetzen (stoppen) |
| `T` | Texturen umschalten (Original/Weiß) |
| `I` | Anweisungen ein-/ausblenden |
| `E` | Erde und Mond umschalten |
| `X, Y, C, B, V` | Easter-Egg-Texturen |
| `ESC` | Beenden |

### Maussteuerung

- **Linke Maustaste + Ziehen**: Kamera rotieren
- **Rechte Maustaste + Ziehen**: Kamera zoomen
- **Mittlere Maustaste + Ziehen**: Kamera verschieben

## Projektstruktur

```
SolarSystem/
├── src/
│   └── SolarSystem/
│       ├── __init__.py          # Package-Initialisierung
│       ├── Main.py              # Haupteinstiegspunkt
│       ├── constants.py         # Konfiguration & Konstanten
│       ├── CelestialBody.py     # Planet-Klassen & Verwaltung
│       ├── Universe.py          # Umgebung (Licht, Skybox)
│       ├── CameraHandler.py     # Kamera-Setup
│       ├── ActionHandler.py     # Benutzereingaben & UI
│       └── SpecialClass.py      # Partikeleffekte
├── models/                      # 3D-Modelle & Texturen
│   ├── planet_sphere.egg.pz     # Planetenmodell
│   ├── solar_sky_sphere.egg.pz  # Skybox-Modell
│   ├── *_tex.jpg                # Planetentexturen
│   └── fireish.ptf              # Partikelkonfiguration
├── docs/                        # Dokumentation
│   ├── SolarSystemUML.png       # UML-Klassendiagramm
│   ├── SolarSystem.png          # Orbitdiagramm
│   └── Fock_Polydor_SolarSystem.pdf  # Ausführliche Dokumentation
├── requirements.txt             # Python-Abhängigkeiten
├── CHANGELOG.md                 # Änderungsprotokoll
└── README.md                    # Diese Datei
```

## Architektur

### Klassendiagramm

![UML Klassendiagramm](docs/SolarSystemUML.png)

### Hauptkomponenten

| Klasse | Beschreibung |
|--------|--------------|
| `Main` | Initialisiert alle Subsysteme und startet die Anwendung |
| `Planet` | Repräsentiert einen einzelnen Himmelskörper |
| `CelestialBody` | Verwaltet alle Planeten und deren Animationen |
| `Universe` | Erstellt Beleuchtung und Sternenhimmel |
| `CameraHandler` | Konfiguriert Kameraposition und Trackball |
| `ActionHandler` | Verarbeitet Tastatureingaben und UI |
| `SpecialClass` | Erzeugt Partikeleffekte für die Sonne |

### Planetendaten

Die Simulation verwendet realistische Verhältnisse (skaliert):

| Planet | Orbitdistanz (AU) | Größe | Umlaufzeit |
|--------|-------------------|-------|------------|
| Merkur | 0.38 | 0.385x | 0.241 Jahre |
| Venus | 0.72 | 0.923x | 0.615 Jahre |
| Erde | 1.00 | 1.000x | 1.000 Jahre |
| Mond | 0.10 (rel.) | 0.100x | 0.075 Jahre |
| Mars | 1.52 | 0.515x | 1.881 Jahre |
| Jupiter | 2.00 | 0.923x | 3.000 Jahre |

## Konfiguration

Alle Einstellungen befinden sich in `src/SolarSystem/constants.py`:

```python
# Simulationsparameter
SIZE_SCALE = 0.6          # Planetengrößen-Multiplikator
ORBIT_SCALE = 10          # Orbitdistanz-Multiplikator
YEAR_SCALE = 60           # Jahr-Dauer in Sekunden
DAY_SCALE = YEAR_SCALE / 365.0 * 5  # Tag-Dauer

# Kamera-Einstellungen
CAMERA_POSITION = (0, 0, 45)
CAMERA_ORIENTATION = (0, -90, 0)
```

### Neue Planeten hinzufügen

Planeten können einfach in `constants.py` hinzugefügt werden:

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

## Entwicklung

### Code-Stil

- Python 3 kompatibel
- Docstrings für alle Klassen und Methoden
- Konstanten in `constants.py` zentralisiert
- Fehlerbehandlung für Asset-Laden

### Erweiterungsmöglichkeiten

- [ ] Weitere Planeten (Saturn, Uranus, Neptun)
- [ ] Asteroidengürtel
- [ ] Raumschiff-Navigation
- [ ] Informations-Overlays für Planeten
- [ ] Sound-Effekte
- [ ] Zeitraffer-Funktion

## Autoren

**Fock & Polydor**

## Lizenz

Dieses Projekt wurde im Rahmen eines Bildungsprojekts erstellt.

## Dokumentation

Weitere Details finden Sie in der ausführlichen Dokumentation:
- [PDF-Dokumentation](docs/Fock_Polydor_SolarSystem.pdf)
- [UML-Diagramm](docs/SolarSystemUML.png)
