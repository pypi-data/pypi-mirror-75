import json
import websockets
import asyncio
import nest_asyncio


def connect(System, input_type="JSON", output_type="JSON", name="Local Model", examples=[]):
    system = System()
    nest_asyncio.apply()
    
    asyncio.get_event_loop().run_until_complete(
        proxy(system, input_type, output_type, name, examples)
    )


async def proxy(system, input_type, output_type, name, examples):
    uri = "wss://beta.catacomb.ai/ws/proxy/"
    async with websockets.connect(uri) as websocket:
        model_id = ""
        await websocket.send(json.dumps({
            "type": "types",
            "input_type": input_type,
            "output_type": output_type,
            "name": name,
            "examples": examples
        }))

        while True:
            text_data = await websocket.recv()
            data = json.loads(text_data)
            if data["type"] == "connect":
                model_id = data["id"]
                print(f"🤖 Success! View your system at https://view.catacomb.ai/local/{model_id}/")
            elif data["type"] == "request":
                req = data["request"]["input"]
                req_id = data["req_id"]
                output = system.output(req)
                await websocket.send(json.dumps({
                    "type": "response",
                    "response": output,
                    "req_id": req_id,
                }))