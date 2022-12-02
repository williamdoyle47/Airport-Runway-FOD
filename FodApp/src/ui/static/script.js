"use strict";

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

class App {
  #map; //adding # makes it private
  #mapZoomLevel = 14;
  #mapEvent;
  #objects = [];
  #coords = [];

  constructor() {
    // Get uers's position
    this._getPosition();
    // this._getCamera();

    // apilist.addEventListener("click", this._moveToPopup.bind(this));
  }

  _getCamera() {
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
          showVideo.srcObject = stream;
        })
        .catch(function (_error) {
          console.log("Something went wrong!");
        });
    }
  }

  _getPosition() {
    if (navigator.geolocation)
      navigator.geolocation.getCurrentPosition(
        this._loadMap.bind(this),
        function () {
          alert(`could not get your position`);
        }
      );
  }
  _loadMap(position) {
    const coords = [44.8830312, -93.2151078]; // MSP Airport

    this.#map = L.map("map").setView(coords, this.#mapZoomLevel);

    L.tileLayer("http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
      attribution: "",
    }).addTo(this.#map);

    // //Handling clicks on map
    // this.#map.on("click", this._showEntry.bind(this));
  }
  // _renderLogData;
  _renderLog(data) {
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
    ${data.coord}
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
  _getApiData() {
    fetch("http://127.0.0.1:8000/logs")
      .then((res) => {
        if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
        return res.json();
      })
      .then((data) => {
        Object.entries(data).forEach(([key, value]) => {
          this._renderLog(value);
        });
        this.#objects.push(data);
        this.#objects.forEach((item) => {
          const id = item.map((log) => log.id);
          const coord = item.map((log) => log.coord);
          coord.forEach((point) => {
            point.split(",");
            const long = point.split(", ");
            const addcoord = long.map(Number);
            console.log(addcoord);
            const marker = new L.marker(addcoord);
            marker
              .addTo(this.#map)
              .bindPopup(`Fod details go here...`)
              .openPopup();
          });
        });
      })
      .catch((err) => console.log(`Error: ${err.message}`));
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

// live video permission
async function getMedia() {
  tooltip.style.display = "none";
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  } catch (err) {
    alert("No Camera access. Please allow access to continue" + err);
  }
}

function getCam() {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
      })
      .catch(function (error) {
        // console.log("No Camera access. Please allow access to continue");
        alert("No Camera access. Please allow access to continue");
      });
  }
}

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
  getCam();
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
