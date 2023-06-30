from django.http import HttpResponse
from .tasks import send_mail_fun
import json
def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("Sent")

import asyncio
import websocket
import threading

#def send_packet(request):
#    asyncio.run(receive_messages())
#    return HttpResponse("Good")


def run_websocket():
    def on_message(ws, message):
        # Process the received message
        print("Received message:", message)



    # Create a WebSocket connection
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/fetch_new_alert/1a/")

    # Set the callback function for incoming messages
    ws.on_message = on_message


    # Start the WebSocket connection
    ws.run_forever()



async def main():
    # Run the WebSocket client in a separate thread
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    # Run the asyncio event loop in the main thread
    while True:
        # Perform other asyncio-related tasks here if needed
        await asyncio.sleep(1)
# Create your views here.
# Disable SSL certificate verification if needed
def send_packet(request):
    # Run the asyncio event loop
    asyncio.run(main())