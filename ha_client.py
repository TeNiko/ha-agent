import os
import requests
from dotenv import load_dotenv

load_dotenv()
HA_URL = os.getenv("HA_URL")
HEADERS = {"Authorization": f"Bearer {os.getenv('HA_TOKEN')}"}


def ha_get(pfad):
    """Schickt eine GET-Anfrage an HA und gibt die Antwort als Python-Daten zurück."""
    antwort = requests.get(f"{HA_URL}{pfad}", headers=HEADERS, timeout=10)
    antwort.raise_for_status()      # wirft einen Fehler bei 401, 404 usw.
    return antwort.json()

def ha_post(pfad, daten):
    """Schickt eine POST-Anfrage mit JSON-Daten an HA."""
    antwort = requests.post(f"{HA_URL}{pfad}", headers=HEADERS, json=daten, timeout=10)
    antwort.raise_for_status()
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


def set_light(entity_id, an, helligkeit=None, farbtemperatur=None):
    """Schaltet ein Licht an oder aus. Helligkeit optional in Prozent (1–100).
      Farbtemperatur optional in Kelvin (2700-6500), eine kleinere Zahl bedeutet wärmeres Licht, eine größere kühleres Licht."""
    erlaubte_ids = [licht["entity_id"] for licht in get_lights()]
    if entity_id not in erlaubte_ids:
        return {"fehler": f"Unbekanntes Licht: {entity_id}. Verfügbar: {erlaubte_ids}"}

    if an:
        daten = {"entity_id": entity_id}
        if helligkeit is not None:
            daten["brightness_pct"] = helligkeit
        if farbtemperatur is not None:
            daten["color_temp_kelvin"] = farbtemperatur
        ha_post("/api/services/light/turn_on", daten)
    else:
        ha_post("/api/services/light/turn_off", {"entity_id": entity_id})

    return {"ok": True, "entity_id": entity_id, "an": an}



if __name__ == "__main__":          # läuft nur, wenn du DIESE Datei direkt startest
    for licht in get_lights():
        print(licht)
    for sensor in get_sensors("Temperatur"):
        print(sensor)
