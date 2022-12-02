import PySimpleGUI as sg

# init Windows Manager
sg.theme("Black")

# def webcam columns
cameracolumn_layout = [[sg.Text("Choose how many camera's you want to display", size=(60,1))], [sg.Combo(["1", "2", "3", "4", "5"], key="cameraAmount", default_value="1")]]

cameracolumn = sg.Column(cameracolumn_layout, element_justification='center', background_color="black")

mapbutton_layout = [[sg.Text("Open Map", size=(60,1), justification='center')], [sg.Button('Map')]]

mapbutton = sg.Column(mapbutton_layout, element_justification='center', background_color="black")

gpsToggle_layout = [[sg.Text("Toggle GPS tracking", size=(60,1), justification='center')], [sg.Button('GPS')]]

gpsToggleButton = sg.Column(gpsToggle_layout, element_justification='center', background_color="black")

threshcolumn_layout = [[sg.Text("Choose the threshold you want to use (%)", size=(60,1))], [sg.Combo(["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"], key='threshAmount', default_value="60")]]

threshcolumn = sg.Column(threshcolumn_layout, element_justification='center', background_color="black")

colwebcam1_layout = [[sg.Text("Camera 1 (Front Driver)", size=(60, 1), background_color='black', justification="center")],
                        [sg.Image(filename="", key="cam1")], [sg.Combo(["1", "2", "3", "4", "5"], key="choice1", default_value="1")]]
colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center', key="cam1Update", background_color='black')

colwebcam2_layout = [[sg.Text("Camera 2 (Front Passenger)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam2")], [sg.Combo(["1", "2", "3", "4", "5"], key="choice2", default_value="2")]]
colwebcam2 = sg.Column(colwebcam2_layout, element_justification='center', key="cam2Update", background_color='black')

colwebcam3_layout = [[sg.Text("Camera 3 (Driver Side)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam3")], [sg.Combo(["1", "2", "3", "4", "5"], key="choice3", default_value="3")]]
colwebcam3 = sg.Column(colwebcam3_layout, element_justification='center', key="cam3Update", background_color='black')

colwebcam4_layout = [[sg.Text("Camera 4 (Passenger Side)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam4")], [sg.Combo(["1", "2", "3", "4", "5"], key="choice4", default_value="4")]]
colwebcam4 = sg.Column(colwebcam4_layout, element_justification='center', key="cam4Update", background_color='black')

colwebcam5_layout = [[sg.Text("Camera 5 (Rear)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam5")], [sg.Combo(["1", "2", "3", "4", "5"], key="choice5", default_value="5")]]
colwebcam5 = sg.Column(colwebcam5_layout, element_justification='center', key="cam5Update", background_color='black')

coltextbox_layout = [[sg.Text("Output", size=(60,1), justification="center")],
                        [sg.Multiline(size=(60, 30), key="textbox", autoscroll=True, disabled=True)]]
coltextbox = sg.Column(coltextbox_layout, element_justification='center')

colslayout = [[cameracolumn, mapbutton, gpsToggleButton, threshcolumn], [colwebcam1, colwebcam2, colwebcam3], [colwebcam4, colwebcam5, coltextbox]]

layout = [colslayout]