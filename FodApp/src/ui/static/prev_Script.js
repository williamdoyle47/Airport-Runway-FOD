"use strict";

const form = document.querySelector(".options");
const containerWorkouts = document.querySelector(".buttons");
const showMap = document.getElementById("map");
const showVideo = document.getElementById("cam");
const video = document.getElementById("videoE");
const switchButtons = document.getElementById("switchButtons");

class App {
  #map; //adding # makes it private
  #mapZoomLevel = 14;
  #mapEvent;
  myVideoInputs = [];
  //   #workouts = [];

  constructor() {
    // Get uers's position
    this._getPosition();
    // this._getCamera();
  }

  _getCamera() {
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
          console.log("Video is streaming")
          showVideo.srcObject = stream;
        })
        .catch(function (_error) {
          console.log("Something went wrong!");
        });
    }
  }
   
  __doGetDevicesInfo = async () => {
      await navigator.mediaDevices.enumerateDevices()
      .then(results => {
              results.forEach(result => {
              console.log(result)
              if(result.kind == 'videoinput'){
                  myVideoInputs.push(result);
              }
          })
      }
      )
      .catch(error => {
          console.log(error);
      })

  }
  __startCamera = async (myVideoInput, whichCamera) => {
      if(myVideoInput === undefined) {console.log('Undefined input'); return;}
      await navigator.mediaDevices.getUserMedia({
          video: {
              width: 200,
              height: 100,
              deviceId: myVideoInput.deviceId
          }
      }).then(stream => {
          whichCamera.srcObject = stream; 
      }).catch(error => {
          console.log(error)
      })
  }
  // __doStartCamera = (button) => {
  //     const id = button.id;
  //     switch(id){
  //         case 'startCamera1':
  //             startCamera(myVideoInputs[1], camera1);
  //             break; 
  //         case 'startCamera2':
  //             startCamera(myVideoInputs[2], camera2);
  //             break; 
  //     }
  // }

  _getPosition() {
    if (navigator.geolocation)
      navigator.geolocation.getCurrentPosition(
        this._loadMap.bind(this),
        function () {
          alert(`could not get your position`);
        }
      );
  }

 

  async _loadMap(position) {
    // this._getPosition();
    //use api to get coordinates
    // const { latitude } = position.coords;
    // const { longitude } = position.coords;
    // console.log(`https://www.google.pt/maps/@${latitude},${longitude}`);

    // const coords = [latitude, longitude]; // Current position
    const coords = [44.8830312, -93.2151078]; // MSP Airport

    this.#map = L.map("map").setView(coords, this.#mapZoomLevel);

    L.tileLayer("http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.#map);

    try {
      console.log("Fetching map data...")
      const response = await fetch("http://127.0.0.1:8000/json", {
        method: "GET",
      });
      if (response.ok) {
        const jsonResponse = await response.json();
        console.log(jsonResponse)
        jsonResponse["Map Points"].forEach((x, i) => {
          var coord = x["coord"].split(',');
          console.log(coord)
          coord = coord.map(Number) 
          console.log(coord)
          var marker = new L.Marker(coord);
          marker.addTo(this.#map).on('click',function({}){
            console.log(x['fod_type'])
            
          });
        });

        // return jsonResponse;
      }
    } catch (error) {
      console.log(error);
    }

    // //Handling clicks on map
    // this.#map.on("click", this._showEntry.bind(this));
  }
  _showEntry(mapE) {
    this.#mapEvent = mapE;
    // form.classList.remove("hidden");
  }
  // to clear the data
  reset() {
    localStorage.removeItem("option");
    location.reload();
  }
  // simply type 'app.reset()' in the console to reset app.
}
const app = new App();
async function renderImage(ctx, blob) {
  const bmp = await createImageBitmap(blob);
  ctx.drawImage(bmp, 0, 0);
  bmp.close();
}

async function capture() {
      // Render image to canvas
  let drawImage = async function(time) {
      prevCtx.drawImage(player, 0, 0, pW, pH);
      const blob = await new Promise(resolve => preview.toBlob(resolve, 'image/jpeg', 0.5));
      socket.send(blob);
      requestAnimationFrame(drawImage);
    };
    requestAnimationFrame(drawImage);
}

function getCam() {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(async function (stream) {
        video.srcObject = stream;
        
        const wss = new WebSocket('ws://localhost:8080/ws', 'echo-protocol');
        wss.addEventListener('open', (event) => {
          console.log("connected to ws")
          capture();
        });
        wss.addEventListener('message', (event) => {
          console.log("message rcvd")
          let blob = event.data;
          renderImage(dCtx, blob);
        });


      })
      .catch(function (error) {
        alert("No Camera access. Please allow access to continue");
      });
  }
}

function swap() {
  getCam();
  if (showVideo.style.display == "none") {
    // alert("Turning on Camera. ");
    showMap.style.display = "none";
    showVideo.style.display = "block";
    showVideo.style.backgroundColor = "white";
    switchButtons.innerHTML = "<i class='fa-regular fa-map'></i>";
  } else {
    showMap.style.display = "block";
    showVideo.style.display = "none";
    switchButtons.innerHTML = "<i class='fa-solid fa-video'></i>";
  }
}

function test(){
  console.log("JHrllo")
}

//API test call


