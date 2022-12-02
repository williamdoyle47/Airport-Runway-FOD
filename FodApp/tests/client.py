import websockets
import asyncio
import cv2
import json
from FodApp.gps_controller import GPS_Controller
#capture video stream
camera = cv2.VideoCapture(2) #Webcam



async def main():
    #initalize GPS
    gps_controller = GPS_Controller()
    try:  # if gps is accessible
        starting_coords = gps_controller.extract_coordinates()
    except:  # if unable to access gps
        starting_coords = [0, 0]
        print("unable to get starting coordinates - defaulting to 0,0")

    # Connect to the server
    async with websockets.connect('ws://localhost:8000/ws') as ws:
         while True:
            success, frame = camera.read()
            if not success:
                print("not success")
                break
            else:
                #capture and send GPS location
                # ret, buffer = cv2.imencode('.png', frame) #explore
                # frame = frame.tolist()
                
                # ws_data = {'buffer': frame, 'coor': gps_controller.extract_coordinates()}
                # ws_data = json.dumps(ws_data).encode('utf-8')
                ret, buffer = cv2.imencode('.png', frame) #explore
                await ws.send(buffer.tobytes())
# Start the connection
asyncio.run(main())