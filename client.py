import websockets
import asyncio
import cv2

#capture video stream
camera = cv2.VideoCapture(2) #Webcam



async def main():
    # Connect to the server
    async with websockets.connect('ws://localhost:8000/ws') as ws:
         while True:
            success, frame = camera.read()
            if not success:
                print("not success")
                break
            else:
                #capture and send GPS location
                ret, buffer = cv2.imencode('.png', frame) #explore
                await ws.send(buffer.tobytes())

# Start the connection
asyncio.run(main())