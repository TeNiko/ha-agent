import os                        # Zugriff auf Umgebungsvariablen
import requests                  # HTTP-Anfragen schicken
from dotenv import load_dotenv   # .env-Datei einlesen

load_dotenv()                    # lädt alle Werte aus .env in die Umgebung

ha_url = os.getenv("HA_URL")     # holt einen Wert anhand seines Namens
ha_token = os.getenv("HA_TOKEN")

headers = {
    "Authorization": f"Bearer {ha_token}",   # so weist du dich bei HA aus
}

antwort = requests.get(f"{ha_url}/api/", headers=headers)

print(antwort.status_code)       # 200 = ok, 401 = Token falsch
print(antwort.json())            # Antwort von HA als Python-Dictionary



