import json
import anthropic
from ha_client import get_lights, get_sensors, set_light   # eigene Funktionen!

client = anthropic.Anthropic()

# Tools beschreiben: Claude sieht nur die Beschreibungen
tools = [
    {
        "name": "get_sensors",
        "description": "Liefert Sensoren aus Home Assistant mit Wert und Einheit. "
                       "Optional nach einem Wort im Namen filtern, z.B. 'Temperatur'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "suchwort": {"type": "string", "description": "Filterwort, leer = alle"}
            },
            "required": [],
        },
    },
    {
        "name": "get_lights",
        "description": "Liefert Lichter aus Home Assistant mit Name und Zustand.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "set_light",
        "description": "Schaltet ein Licht an oder aus. Verwende die entity_id aus get_lights. "
                       "Helligkeit nur angeben, wenn der Nutzer sie nennt."
                       "Farbtemperatur nur angeben, wenn der Nutzer sie nennt. Eine kleinere Zahl bedeutet wärmeres Licht, eine größere kühleres Licht.",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string", "description": "z.B. light.stehlampe"},
                "an": {"type": "boolean", "description": "true = an, false = aus"},
                "helligkeit": {"type": "integer", "minimum": 1, "maximum": 100,
                               "description": "Helligkeit in Prozent, optional"},
                "farbtemperatur": {"type": "integer", "minimum": 2700 , "maximum": 6500,
                                   "description": "Farbtemperatur in Kelvin, optional"},
            },
            "required": ["entity_id", "an"],
        },
    },

]

# Name → echte Funktion zuordnen
funktionen = {
    "get_sensors": get_sensors,
    "get_lights": get_lights,
    "set_light": set_light,
}

SYSTEM = """Du bist ein Smarthome-Assistent. Antworte kurz auf Deutsch.

Routinen:
- Wenn gesagt wird, dass man weggeht oder schlafen geht (z.B. "Schau, auf wiedersehen, gute Nacht"): alle Lichter ausschalten.
"""


def agent_antwort(messages):
    """Führt den Agent Loop aus, bis Claude fertig ist, und gibt den Antworttext zurück."""
    while True:
        antwort = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=16000,
            system=SYSTEM,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": antwort.content})

        if antwort.stop_reason != "tool_use":
            break

        ergebnisse = []
        for block in antwort.content:
            if block.type == "tool_use":
                print(f"  [Tool: {block.name}({block.input})]")
                try:
                    ergebnis = funktionen[block.name](**block.input)
                    ergebnisse.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(ergebnis, ensure_ascii=False),
                    })
                except Exception as e:
                    print(f"  [Fehler: {e}]")
                    ergebnisse.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Fehler beim Ausführen von {block.name}: {e}",
                        "is_error": True,
                    })
                
        messages.append({"role": "user", "content": ergebnisse})

    return "".join(block.text for block in antwort.content if block.type == "text")

# das Gedächtnis des Chats
messages = []
print("HA-Agent bereit. 'exit' zum Beenden.")

# Gesprächsschleife
while True:                                     
    frage = input("\nDu: ")
    if frage.lower() == "exit":
        break
    messages.append({"role": "user", "content": frage})
    try:
        print(f"Claude: {agent_antwort(messages)}")
    except anthropic.RateLimitError as e:
        print(f"  [Rate-Limit-Fehler: {e}]")
    except anthropic.APIConnectionError as e:
        print(f"  [API-Verbindungsfehler: {e}]")
    
