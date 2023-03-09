const form = document.querySelector(".options");
const apilist = document.querySelector(".api");
const logs = document.querySelector(".logs");
const mySidepanel = document.querySelector(".openbtn");
const tooltip = document.querySelector(".tooltiptext");
const showMap = document.getElementById("map");
const showVideo = document.getElementById("cam");
const video = document.getElementById("videoE");
const switchButtons = document.getElementById("switchButtons");
const sidePanel = document.getElementById("mySidepanel");
const sideCam = document.getElementById("sideCam");
const favicon = document.getElementById("favicon");


class Map{
    coords = [44.8830312, -93.2151078]; // MSP Airport
    mapZoomLevel = 14;
    map = L.map("map").setView(this.coords, this.mapZoomLevel);

    constructor(){
       this._getPosition()
    }

    _getPosition() { //Ask User for location data
        if (navigator.geolocation)
        navigator.geolocation.getCurrentPosition(
            this.__loadmap.bind(this),
            function () {
            alert(`could not get your position`);
            }
        );
    }

    __loadmap(position){ //Render location on leaflet map -- in this case hardset to MSP airport for demo
        L.tileLayer("http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
        attribution: "",
        }).addTo(this.map);
    }

    removeMark(dis, marker){
        console.log(marker)
        this.map.removeLayer(marker);
    }

    addPoint(obj){
        var point = obj.coord
        point.split(",");
        const long = point.split(", ")
        const coord = long.map(Number);

        var fod_type = obj.fod_type
        var timestamp = obj.timestamp
        var recommended_action = obj.recommended_action
        var uuid = obj.uuid
        console.log(uuid)
        console.log(typeof uuid)
        var marker = new L.marker(coord).addTo(this.map)
        var custom_style= {
            maxWidth: 300,
            minWidth: 300,
            closeOnClick: false,
            className: `log-popup`,
        }

        var content = `
            <h2>${fod_type}</h2> 
            <p> Coord: ${coord}</p>
            <p> Time: ${timestamp}</p>
            <p> recommended cleanup action: ${recommended_action}</p>
            <img height=150 width =150 src="http://127.0.0.1:8000/fod_img/${uuid}"> 
        ` 
        marker.bindPopup(content, custom_style)
        console.log(marker)
        // remove on double click

        marker.on('dblclick', ()=> {this.map.removeLayer(marker); 
            fetch('http://127.0.0.1:8000/mark_clean/' + new URLSearchParams({
                uuid
            }), {method: 'PATCH'}).then(response=>response.json())
                                .then(data=>{ console.log(data); })
        })
        //add button and show details + images
    }

}

// later add class Camera to access user cam via browser 

var map = new Map()


function renderLog(data) {
    const html = `
    <ul class="objects_detected">
    <div class="object_row">
      Name: 
    </div>
    <div class="object_row">
    ${data.fod_type}
    </div>
    <div class="object_row">
      Coords:
    </div>  <div class="object_row">
    [${data.coord}]
    </div>
    <div class="object_row">
      Confidence:
    </div>
    <div class="object_row">
    ${data.confidence_level * 100}%
  
  </div>
  </ul>
    `;
    logs.insertAdjacentHTML("beforeend", html);
    logs.style.opacity = 1;
  }

function notification() {
  var audio = new Audio('../static/mixkit-long-pop-2358.wav');
  if (document.visibilityState === "hidden") {
    favicon.setAttribute("href", "../static/img2.png");
  } else {
    audio.play();
  }
}

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    favicon.setAttribute("href", "../static/img1.png");
  }
});

//Socket and Live Feed Functions
socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.onopen = function(event) {
    alert("Connection with WS made")
};

var interval = window.setInterval(function(){
    socket.send("open")
}, 5000)

socket.onmessage = function(event) {
  // Add Data point to map
  var obj = JSON.parse(event.data);
  map.addPoint(obj)

  //add Data point to log
    renderLog(obj)

    notification()
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    alert('[close] Connection died');
  }
};

socket.onerror = function(error) {
  alert(`[error]`);
};

//Display Functions

function displayMap() {
  showMap.style.display = "block";
  showVideo.style.display = "none";
  // switchButtons.innerHTML = "<i class='fa-solid fa-video'></i>";
  sideCam.innerHTML = "<i class='fa-solid fa-video'></i>";
}
function displayCam() {
  // alert("Turning on Camera. ");
  showMap.style.display = "none";
  showVideo.style.display = "block";
  showVideo.style.backgroundColor = "white";
  // switchButtons.innerHTML = "<i class='fa-regular fa-map'></i>";
  sideCam.innerHTML = "<i class='fa-regular fa-map'></i>";
}

function swap() {
  // getCam();
  if (showVideo.style.display == "none") {
    displayCam();
  } else {
    displayMap();
  }
}
function openNav() {
  sidePanel.style.width = "250px";
  mySidepanel.style.display = "none";
  sideCam.style.display = "none";
  form.style.display = "none";
}
function closeNav() {
  sidePanel.style.width = "0";
  mySidepanel.style.display = "block";
  sideCam.style.display = "block";
  form.style.display = "block";
}