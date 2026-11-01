import json
import anthropic
from ha_client import get_lights, get_sensors   # deine eigenen Funktionen!

client = anthropic.Anthropic()

# 1. Tools beschreiben: Claude sieht NUR diese Beschreibung, nicht deinen Code
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
]

# 2. Name → echte Funktion zuordnen
funktionen = {
    "get_sensors": get_sensors,
    "get_lights": get_lights
}

frage = input("Du: ")
messages = [{"role": "user", "content": frage}]

# 3. Der Agent Loop
while True:
    antwort = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=16000,
        system="Du bist ein Smarthome-Assistent. Antworte kurz auf Deutsch.",
        tools=tools,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": antwort.content})

    if antwort.stop_reason != "tool_use":       # Claude ist fertig
        break

    ergebnisse = []
    for block in antwort.content:
        if block.type == "tool_use":
            print(f"  [Tool: {block.name}({block.input})]")      # zum Zuschauen
            ergebnis = funktionen[block.name](**block.input)      # Funktion ausführen
            ergebnisse.append({
                "type": "tool_result",
                "tool_use_id": block.id,                # gehört zu welcher Anfrage
                "content": json.dumps(ergebnis, ensure_ascii=False),
            })
    messages.append({"role": "user", "content": ergebnisse})

# 4. Antwort ausgeben
for block in antwort.content:
    if block.type == "text":
        print(f"Claude: {block.text}")
