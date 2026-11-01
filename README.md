# HA-Agent

## Was ist das?
Mit diesem Projekt kann man mittels eines KI-API-Key sein Home-Assistent steuern.

## Features
- Lichter und Sensoren abfragen
- Lichter ein/aus schalten und Temperatur der Lampen einstellen
- Routinen. Beim Schlafen gehen oder Haus verlassen werden alle Lichter ausgeschaltet

## Setup
> pip install -r requirements.txt
python Version 3.11
eine laufende Home-Assistant-Instanz
Die .env Datei muss mit entsprechend Daten werden.
HA_URL=http://homeassistant.local:8123
HA_TOKEN=dein-ha-token
ANTHROPIC_API_KEY=dein-anthropic-key

## Starten
> python agent.py

## Beenden
Im Chatfenster "exit" eingeben.