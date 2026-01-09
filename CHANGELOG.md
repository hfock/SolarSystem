# Changelog

Alle wesentlichen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [1.0.0] - 2026-01-09

### Hinzugefügt

- **constants.py**: Neues Modul mit allen Konfigurationswerten
  - Zentralisierte Planetendaten (Orbit, Größe, Umlaufzeit)
  - Kamera- und Lichteinstellungen
  - UI-Konstanten
  - Easter-Egg-Textur-Definitionen
- **Planet-Klasse**: Abstrakte Klasse für einzelne Himmelskörper
  - Generisches Laden von Modellen und Texturen
  - Automatische Orbit- und Rotationsanimationen
  - Unterstützung für Mond-Objekte mit Parent-Referenzen
- **requirements.txt**: Python-Abhängigkeiten definiert
- **CHANGELOG.md**: Änderungsprotokoll
- **Umfassendes README.md**: Vollständige Dokumentation mit
  - Installationsanleitung
  - Tastatur- und Maussteuerung
  - Projektstruktur
  - Architekturübersicht
  - Konfigurationsanleitung

### Geändert

- **ActionHandler.py**: Komplett refaktoriert
  - Code-Duplizierung um ~60% reduziert
  - `speedUp()` / `slowDown()` nutzen jetzt Schleifen statt Copy-Paste
  - `loadTex()` / `resumeToNormalTex()` iterieren über Planetenliste
  - Neue Helper-Methoden: `_set_all_play_rates()`, `_adjust_all_play_rates()`
  - Entfernte doppelte Funktionsdefinitionen
  - Docstrings für alle Methoden hinzugefügt

- **CelestialBody.py**: Komplett refaktoriert
  - Neue `Planet`-Klasse für einzelne Himmelskörper
  - Generisches Laden basierend auf Konfiguration aus constants.py
  - Automatische Unterstützung für Monde (Parent-Child-Beziehungen)
  - Legacy-Methoden für Rückwärtskompatibilität beibehalten

- **Universe.py**: Verbessert
  - Konstanten aus constants.py verwendet
  - Schleife für Punktlichter statt 6x Copy-Paste
  - Fehlerbehandlung für Asset-Laden
  - Docstrings hinzugefügt

- **CameraHandler.py**: Verbessert
  - Konstanten aus constants.py verwendet
  - Docstrings hinzugefügt

- **SpecialClass.py**: Verbessert
  - Konstanten aus constants.py verwendet
  - Fehlerbehandlung für Partikelkonfiguration
  - `cleanup()` Methode hinzugefügt
  - Docstrings hinzugefügt

- **Main.py**: Modernisiert
  - Shebang für Python 3 hinzugefügt
  - Flexible Import-Struktur (Modul und Standalone)
  - `main()` Entry-Point-Funktion hinzugefügt
  - Docstrings hinzugefügt

- **__init__.py**: Package-Metadaten hinzugefügt
  - Version und Autor definiert
  - Modul-Dokumentation

### Behoben

- Import-Probleme bei Verwendung als Python-Modul
- Doppelte Funktionsdefinitionen in ActionHandler.py
- Fehlende Fehlerbehandlung bei Asset-Laden

### Technische Verbesserungen

- Python 3 Kompatibilität (f-Strings, moderne Syntax)
- Konsistente Namenskonventionen (snake_case für private Methoden)
- Rückwärtskompatibilität durch Methoden-Aliase
- Reduzierung von Magic Numbers durch Konstanten

## [0.x] - Frühere Versionen

### Features der ursprünglichen Version

- 3D-Darstellung des Sonnensystems mit Panda3D
- 7 Himmelskörper: Sonne, Merkur, Venus, Erde, Mond, Mars, Jupiter
- Realistische Orbitalverhältnisse
- Interaktive Steuerung (Pause, Geschwindigkeit, Texturen)
- Partikeleffekte für die Sonne
- Kamerasteuerung mit Trackball

---

## Upgrade-Anleitung

### Von 0.x auf 1.0.0

Die API bleibt rückwärtskompatibel. Alle bestehenden Aufrufe funktionieren weiterhin.

**Empfohlene Änderungen:**

1. Verwenden Sie die neuen Konstanten aus `constants.py`:
   ```python
   from SolarSystem.constants import SIZE_SCALE, ORBIT_SCALE
   ```

2. Nutzen Sie die neue `Planet`-Klasse für Erweiterungen:
   ```python
   from SolarSystem.CelestialBody import Planet
   ```

3. Fügen Sie neue Planeten über `constants.py` hinzu statt Code zu ändern.
