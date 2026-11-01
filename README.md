# HA-Agent

## Was ist das?
HA-Agent ist ein selbst gebauter KI-Agent, mit dem sich ein Home Assistant
per natürlicher Sprache steuern lässt. Statt fester Befehle versteht er
Sätze wie „Mach's gemütlich“ oder „Ich geh jetzt schlafen" und setzt
sie selbstständig in die passenden Aktionen um.

Technisch nutzt der Agent die Claude-API mit **Tool Use**: Claude entscheidet,
welche Funktionen aufgerufen werden, der Python-Code führt sie über die
Home-Assistant-REST-API aus und meldet das Ergebnis zurück. Der Agent Loop
ist von Grund auf selbst implementiert, ohne Agent-Framework.

## Features
- Lichter und Sensoren abfragen
- Lichter ein/aus schalten und Farbtemperatur einstellen
- Routinen. Beim Schlafen gehen oder Haus verlassen werden alle Lichter ausgeschaltet

## Wie funktioniert es?

```
Nutzer → agent.py → Claude-API (mit Tool-Beschreibungen)
                         ↓
              Claude wählt ein Tool + Parameter
                         ↓
         ha_client.py → Home-Assistant-REST-API → Gerät
                         ↓
              Ergebnis zurück an Claude → Antwort an Nutzer
```

1. Die Nutzereingabe wird zusammen mit den verfügbaren Tools an Claude geschickt.
2. Claude entscheidet, ob und welches Tool gebraucht wird (z. B. `get_lights`, `set_light`).
3. Der Python-Code führt das Tool aus und schickt das Ergebnis zurück.
4. Das wiederholt sich, bis Claude alle Informationen hat. So entstehen
   auch mehrstufige Abläufe, z. B. erst Lichter abfragen, dann gezielt schalten.
5. Der Gesprächsverlauf bleibt erhalten, dadurch versteht der Agent auch
   Rückbezüge wie „etwas wärmer bitte“.

**Projektstruktur**
- `agent.py`: Chat, Agent Loop, Tool-Definitionen und System-Prompt mit Routinen
- `ha_client.py`: Funktionen für den Zugriff auf die Home-Assistant-API

## Sicherheit & Robustheit

- **Least Privilege:** Der Agent bekommt nur Tools für das, was er wirklich
  darf. Geräte wie z.B. Steckdosen kann er bewusst nur lesen, nicht schalten, weil dafür kein
  Tool existiert.
- **Validierung:** Vor jedem Schaltbefehl wird geprüft, ob die `entity_id`
  existiert. Erfundene Geräte werden abgelehnt, und Claude bekommt die Liste
  der gültigen Geräte zurück.
- **Fehler als Rückmeldung statt Absturz:** Schlägt ein Tool fehl, erhält
  Claude die Fehlermeldung (`is_error`) und kann dem Nutzer erklären, was
  passiert ist.
- **Timeouts:** Anfragen an Home Assistant brechen nach 10 Sekunden ab,
  statt endlos zu hängen.
- **API-Fehler:** Verbindungsprobleme oder Rate Limits der Claude-API
  beenden den Chat nicht.
- **Secrets:** Token und API-Key liegen in der `.env` und sind per
  `.gitignore` vom Repository ausgeschlossen.

## Stand & Roadmap

- ✅ **Meilenstein 1:** Lichter und Sensoren abfragen
- ✅ **Meilenstein 2:** Lichter schalten, dimmen, Farbtemperatur einstellen
- ✅ **Meilenstein 3:** Chat mit Gedächtnis und Routinen
- ⏳ **Meilenstein 4:** Lokales LLM einbinden


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

```
HA_URL=http://homeassistant.local:8123
HA_TOKEN=dein-ha-token
ANTHROPIC_API_KEY=dein-anthropic-key
```

Den HA-Token erstellst du in Home Assistant unter *Profil → Sicherheit → Langlebige Zugangs-Token*.

### Starten
```
python agent.py
```
Mit `exit` beendest du den Chat.
