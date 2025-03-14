import asyncio
import websockets
import json
import keyboard

# Dictionary to store connected clients: websocket -> device_type ("pc" or "android")
connected_clients = {}

# Function to control media on the PC using the keyboard module
def control_media_on_pc(action):
    print(f"Executing media control on PC: {action}")
    try:
        if action in ["play", "pause", "toggle_play_pause"]:
            keyboard.send("play/pause media")
        elif action == "next":
            keyboard.send("next track")
        elif action == "prev":
            keyboard.send("previous track")
        elif action == "volume_up":
            keyboard.send("volume up")
        elif action == "volume_down":
            keyboard.send("volume down")
        elif action == "mute":
            try:
                keyboard.send("mute")
            except Exception as e:
                print("Mute key not supported:", e)
        else:
            print("Unknown action:", action)
    except Exception as e:
        print("Error executing media command:", e)

# Register a new client by waiting for an initial message that identifies the device type.
async def register_client(websocket):
    try:
        # Expecting an init message in JSON format, e.g.:
        # { "init": true, "device": "android" } or { "init": true, "device": "pc" }
        init_message = await asyncio.wait_for(websocket.recv(), timeout=10)
        data = json.loads(init_message)
        if data.get("init"):
            device_type = data.get("device", "unknown")
            connected_clients[websocket] = device_type
            print(f"Registered client as {device_type}")
            await websocket.send(f"Registered as {device_type}")
    except Exception as e:
        print("Registration failed:", e)
        connected_clients[websocket] = "unknown"

# Remove a client from the registry when it disconnects.
async def unregister_client(websocket):
    if websocket in connected_clients:
        print(f"Client {connected_clients[websocket]} disconnected")
        del connected_clients[websocket]

# Broadcast a message to all clients of a different device type than the sender.
async def broadcast_to_others(sender, message):
    sender_type = connected_clients.get(sender, "unknown")
    for client, device_type in connected_clients.items():
        if client != sender and device_type != sender_type:
            try:
                await client.send(message)
            except Exception as e:
                print("Error broadcasting to client:", e)

# The main WebSocket connection handler.
async def handle_connection(websocket, path=None):
    # First, register the client with its device type.
    await register_client(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Try to parse the message as JSON
            try:
                data = json.loads(message)
                action = data.get("action", "")
            except Exception as e:
                action = message  # Fallback if not JSON

            sender_type = connected_clients.get(websocket, "unknown")
            print(f"Command from {sender_type}: {action}")

             # Forward the command to clients of the other device type.
            await broadcast_to_others(websocket, json.dumps({"action": action}))
            # Process the command locally on the PC regardless of who sent it.
            control_media_on_pc(action)

    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected unexpectedly")
    except Exception as e:
        print("Error in connection:", e)
    finally:
        await unregister_client(websocket)
        

# Main function to start the WebSocket server.
async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run indefinitely

if __name__ == "__main__":
    asyncio.run(main())

