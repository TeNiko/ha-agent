import os
import requests
from dotenv import load_dotenv

load_dotenv()
ha_url = os.getenv("HA_URL")
ha_token = os.getenv("HA_TOKEN")
headers = {"Authorization": f"Bearer {ha_token}"}

antwort = requests.get(f"{ha_url}/api/states", headers=headers)
geraete = antwort.json()                    # Liste von Dictionaries

print(f"{len(geraete)} Entitäten gefunden") # len() = Anzahl Elemente

for geraet in geraete:                      # geht jedes Element nacheinander durch
    if geraet["entity_id"].startswith("light."):   # nur Lichter
        name = geraet["attributes"]["friendly_name"] # verschachtelter Zugriff
        zustand = geraet["state"]
        print(f"{name}: {zustand}")
