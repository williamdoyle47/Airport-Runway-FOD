"use strict";

const form = document.querySelector(".options");
const apilist = document.querySelector(".api");
const logs = document.querySelector(".logs");
const popUpHtml = document.querySelector(".leaflet-popup-content");
const box = document.getElementById("chkBox");
const mySidepanel = document.querySelector(".openbtn");
const tooltip = document.querySelector(".tooltiptext");
const showMap = document.getElementById("map");
const showVideo = document.getElementById("cam");
const video = document.getElementById("videoE");
const switchButtons = document.getElementById("switchButtons");
const sidePanel = document.getElementById("mySidepanel");
const sideCam = document.getElementById("sideCam");

const url = "http://127.0.0.1:8000/all_logs";
const TIMEOUT_SEC = 10;
let marker;
let title;

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
  _loadMap() {
    const coords = [44.8830312, -93.2151078]; // MSP Airport

    this.#map = L.map("map").setView(coords, this.#mapZoomLevel);

    L.tileLayer("http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
      attribution: "",
    }).addTo(this.#map);

    // //Handling clicks on map
    // this.#map.on("click", this._showEntry.bind(this));
  }
  // _renderLogData(data)

  _renderLog(data) {
    const html = `
    <ul class="objects_detected">
    <div class="object_row">
      Type: 
    </div>
    <div class="object_row">
    ${data.fod_type}
    </div>
    <div class="object_row">
      Coords:
    </div>  
    <div class="object_row">
    [${data.coord}]
    </div>
    <div class="object_row">
      Confidence:
    </div>
    <div class="object_row">
    ${(data.confidence_level * 100).toFixed(2)}%
    </div>
    </ul>
    `;
    logs.insertAdjacentHTML("beforeend", html);
    logs.style.opacity = 1;
  }

  //New method
  _timeout = function (s) {
    return new Promise(function (_, reject) {
      setTimeout(function () {
        reject(new Error(`Request took too long! Timeout after ${s} second`));
      }, s * 1000);
    });
  };

  _loadFod = async function () {
    try {
      const data = fetch("http://127.0.0.1:8000/all_logs");
      const res = await Promise.race([data, this._timeout(TIMEOUT_SEC)]);
      const dataRes = await res.json();

      if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
      dataRes.forEach((fodDetails) => {
        //add fod details to the colomn
        this._renderLog(fodDetails);

        //Create variable details
        const id = fodDetails.id;
        const fod_type = fodDetails.fod_type;
        const confLvl = (fodDetails.confidence_level * 100).toFixed(2);
        const image = fodDetails.image_path;
        const cleaned = fodDetails.cleaned;
        const recAction = fodDetails.recommended_action;
        const time = fodDetails.timestamp;

        //create coordinates
        const points = fodDetails.coord;
        points.split(",");
        const long = points.split(", ");
        const addcoord = long.map(Number);
        console.log(addcoord);

        //add Marker
        marker = new L.marker(addcoord);
        marker.addTo(this.#map).bindPopup(
          L.popup({
            maxWidth: 220,
            minWidth: 160,
            // closeOnClick: false,
            closeOnClick: true,
            className: `log-popup`,
            opacity: 0.5,
          })
        ).setPopupContent(`
          Id: ${id} <br>
          Type: ${fod_type} <br>
          Confidence: ${confLvl}% <br>
          Image: ${image} <br>
          Rec. Action: ${recAction} <br>
          <br>
          <div>
          <input type="checkbox" id="chkBox" style=""><hr>Cleared
          </div>
          `);
        // .openPopup();
      });
    } catch (err) {
      throw err;
    }
  };

  //Check box
  _checkBox() {
    box.checked = false;
  }

  /*
  //Old method
  _getApiData() {
    // fetch("http://127.0.0.1:8000/all_uncleaned")
    fetch("http://127.0.0.1:8000/all_logs")
      .then((res) => {
        if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
        return res.json();
      })
      .then((data) => {
        Object.entries(data).forEach(([key, value]) => {
          this._renderLog(value);
          // console.log(value);
        });
        this.#objects.push(data);
        this.#objects.forEach((item) => {
          /*
          const id = item.map((log) => log.id);
          const imagePath = item.map((log) => log.image_path);
          const timestamp = item.map((log) => log.timestamp);
          
          const recAction = item.map((log) => log.recommended_action);
          const confLvl = item.map((log) => log.confidence_level);
          const fod_type = item.map((log) => log.fod_type);
          */
  /*
          const coord = item.map((log) => log.coord);
          coord.forEach((point) => {
            console.log(point);
            point.split(",");
            const long = point.split(", ");
            const addcoord = long.map(Number);
            // console.log(addcoord);

            // console.log(addcoord);
            marker = new L.marker(addcoord);
            marker.addTo(this.#map).bindPopup(
              L.popup({
                maxWidth: 250,
                minWidth: 200,
                closeOnClick: false,
                className: `log-popup`,
              })
            ).setPopupContent(`
              Name: ${title} <br>
              Coords: [${addcoord}] <br>

              `);
            // .openPopup();
          });
        });
      })
      .catch((err) => console.log(`Error: ${err.message}`));
  }
  */
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
// async function getMedia() {
//   tooltip.style.display = "none";
//   try {
//     const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//   } catch (err) {
//     alert("No Camera access. Please allow access to continue" + err);
//   }
// }

// function getCam() {
//   if (navigator.mediaDevices.getUserMedia) {
//     navigator.mediaDevices
//       .getUserMedia({ video: true })
//       .then(function (stream) {
//         video.srcObject = stream;
//       })
//       .catch(function (error) {
//         // console.log("No Camera access. Please allow access to continue");
//         alert("No Camera access. Please allow access to continue");
//       });
//   }
// }

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
