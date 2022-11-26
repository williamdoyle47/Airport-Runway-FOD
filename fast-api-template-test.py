import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse

from DetectionLogging import LogDetection

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cameras")
def home(request: Request):
    return templates.TemplateResponse("cameras.html", {"request": request})

@app.get("/json", response_class=ORJSONResponse)
async def send_data_points():
    try:
        #read all data last 24hrs (unless cleaned up)
        det_log = LogDetection()
        #format data
        items = det_log.read_map_points()
        json_list = []
        for item in items:
            type = item[0]
            coor = item[1]
            timestamp = item[2]
            confidence = item[3]
            json = {"fod_type": type, "coord": coor, "timestamp": 
                timestamp, "confidence": confidence}
            json_list.append(json)
        #send data
        return {"Map Points": json_list}
    except:
        return [{"message": "failure to render map points"}]



if __name__ == '__main__':
    uvicorn.run("fast-api-template-test:app", reload=True)


