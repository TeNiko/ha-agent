# HA-Agent

## Was ist das?
HA-Agent ist ein selbst gebauter KI-Agent, mit dem sich ein Home Assistant
per natürlicher Sprache steuern lässt. Statt fester Befehle versteht er
Sätze wie „Mach's gemütlich“ oder „Ich geh jetzt schlafen und setzt
sie selbstständig in die passenden Aktionen um.

Technisch nutzt der Agent die Claude-API mit **Tool Use**: Claude entscheidet,
welche Funktionen aufgerufen werden, der Python-Code führt sie über die
Home-Assistant-REST-API aus und meldet das Ergebnis zurück. Der Agent Loop
ist von Grund auf selbst implementiert, ohne Agent-Framework.

## Features
- Lichter und Sensoren abfragen
- Lichter ein/aus schalten und Temperatur der Lampen einstellen
- Routinen. Beim Schlafen gehen oder Haus verlassen werden alle Lichter ausgeschaltet

## Setup

### Voraussetzungen
- Python 3.11 oder neuer
- Eine laufende Home-Assistant-Instanz
- Ein Anthropic-API-Key ([console.anthropic.com](https://console.anthropic.com))

### Installation
```
git clone https://github.com/TeNiko/ha-agent.git
cd ha-agent
pip install -r requirements.txt
```

### Konfiguration
Im Projektordner eine Datei `.env` anlegen und mit folgenden Werten befüllen:

- HA_URL=http://homeassistant.local:8123
- HA_TOKEN=dein-ha-token
- ANTHROPIC_API_KEY=dein-anthropic-key

Den HA-Token erstellst du in Home Assistant unter *Profil → Sicherheit → Langlebige Zugangs-Token*.

### Starten
```
python agent.py
```
Mit `exit` beendest du den Chat.
