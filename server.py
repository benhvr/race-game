import os

import asyncio
import json
import websockets

from drifters_core import GameState

# État global du jeu (un seul joueur pour l'instant)
state = GameState()
inputs = {"z": False, "s": False, "q": False, "d": False}
clients = set()

async def boucle_jeu():
    """ Tourne à 20 Hz, met à jour le jeu et envoie l'état à tous les clients. """
    while state.running:
        state.update(inputs)

        message = json.dumps(state.to_dict())
        # Envoie à tous les clients connectés
        for ws in list(clients):
            try:
                await ws.send(message)
            except:
                clients.discard(ws)  # client déconnecté

        await asyncio.sleep(1 / 20)  # 20 images/seconde

async def gerer_client(websocket):
    """ Gère la connexion d'un client : reçoit ses inputs. """
    clients.add(websocket)
    print(f"Client connecté. Total : {len(clients)}")
    try:
        async for message in websocket:
            data = json.loads(message)
            # data = {"z": bool, "s": bool, "q": bool, "d": bool}
            inputs.update(data)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)
        print(f"Client déconnecté. Total : {len(clients)}")

async def main():
    # Lance la boucle de jeu en parallèle du serveur WebSocket
    port = int(os.environ.get("PORT", 8765))
    asyncio.create_task(boucle_jeu())

    async with websockets.serve(gerer_client, "0.0.0.0", port):
        print(f"Serveur démarré sur {port}")
        await asyncio.Future()  # tourne indéfiniment

asyncio.run(main())
