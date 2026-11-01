import os
import requests
from dotenv import load_dotenv

load_dotenv()
HA_URL = os.getenv("HA_URL")
HEADERS = {"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"}


def ha_get(pfad):
    """Schickt eine GET-Anfrage an HA und gibt die Antwort als Python-Daten zurück."""
    antwort = requests.get(f"{HA_URL}{pfad}", headers=HEADERS)
    antwort.raise_for_status()      # wirft einen Fehler bei 401, 404 usw.
    return antwort.json()


def get_lights():
    """Gibt eine Liste aller Lichter mit Name und Zustand zurück."""
    lichter = []                                # leere Liste
    for geraet in ha_get("/api/states"):
        if geraet["entity_id"].startswith("light."):
            lichter.append({                    # neues Element anhängen
                "entity_id": geraet["entity_id"],
                "name": geraet["attributes"].get("friendly_name", ""),
                "zustand": geraet["state"],
            })
    return lichter

def get_sensors(suchwort=""):
    """Gibt eine Liste aller Sensoren mit Name, Wert und Einheit zurück."""
    sensoren = []
    for geraet in ha_get("/api/states"):
        if geraet["entity_id"].startswith("sensor."):
            name = geraet["attributes"].get("friendly_name", "")

            if suchwort in name:
                sensoren.append({
                    "entity_id": geraet["entity_id"],
                    "name": name,
                    "wert": geraet["state"],
                    "einheit": geraet["attributes"].get("unit_of_measurement","")
                    })
    return sensoren


if __name__ == "__main__":          # läuft nur, wenn du DIESE Datei direkt startest
    for licht in get_lights():
        print(licht)
    for sensor in get_sensors("Temperatur"):
        print(sensor)
