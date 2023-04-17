const form = document.querySelector(".options");
const apilist = document.querySelector(".api");
const logs = document.querySelector(".logs");
const mySidepanel = document.querySelector(".openbtn");
const tooltip = document.querySelector(".tooltiptext");
const radiusbtn = document.querySelector(".radiusbtn");
const feedbtn = document.querySelector(".feedbtn");
var notification = document.querySelector(".notification");
const showMap = document.getElementById("map");
const showVideo = document.getElementById("cam");
const video = document.getElementById("videoE");
const switchButtons = document.getElementById("switchButtons");
const sidePanel = document.getElementById("mySidepanel");
const sideCam = document.getElementById("sideCam");
const favicon = document.getElementById("favicon");
const sideNotif = document.getElementById("sideNotif");
const notifCount = document.getElementById("notifCount");
var uncleanFodCount;

//Server Side Events and Live Feed Functions
const evtSource = new EventSource("http://127.0.0.1:8000/stream");
evtSource.addEventListener("update", function(event) {
  //   // Logic to handle status updates
  //   console.log(event)

  const obj = JSON.parse(event.data);
  map.addPoint(obj);

  uncleanFodCount = uncleanFodCount + 1;
  notifCount.innerHTML = uncleanFodCount;

  //add Data point to log
  renderLog(obj);
});
evtSource.addEventListener("end", function (event) {
  console.log("Handling end....");
  evtSource.close();
});

const TIMEOUT_SEC = 10;

class Map {
  coords = [44.8830312, -93.2151078]; // MSP Airport
  mapZoomLevel = 14;
  map = L.map("map").setView(this.coords, this.mapZoomLevel);

  constructor() {
    this._getPosition();
  }

  _getPosition() {
    //Ask User for location data
    if (navigator.geolocation)
      navigator.geolocation.getCurrentPosition(
        this.__loadmap.bind(this),
        function () {
          alert(`could not get your position`);
        }
      );
  }

  __loadmap(position) {
    //Render location on leaflet map -- in this case hardset to MSP airport for demo
    L.tileLayer("http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
      attribution: "",
    }).addTo(this.map);
  }

  //Fod Count

  //create a timeout function to avoid errors
  _timeout = function (s) {
    return new Promise(function (_, reject) {
      setTimeout(function () {
        reject(new Error(`Request took too long! Timeout after ${s} second`));
      }, s * 1000);
    });
  };

  // Find all available/uncleared FOD in API  
  __addAllUnclean = async function () {
    try {
      // const data = fetch("http://127.0.0.1:8000/all_logs");
      const data = fetch("http://127.0.0.1:8000/all_uncleaned");
      const res = await Promise.race([data, this._timeout(TIMEOUT_SEC)]);
      const dataRes = await res.json();
      uncleanFodCount = dataRes.length;
      notifCount.innerHTML = uncleanFodCount;

      /* Display all uncleared FOD in side panel and the map*/

      dataRes.forEach((fod) => {
        this.addPoint(fod);
      });
      if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
    } catch (err) {
      throw err;
    }
  };

  removeMark(dis, marker) {
    console.log(marker);
    this.map.removeLayer(marker);
  }

  addPoint(obj) {
    //create lat and long values
    const point = obj.coord;
    point.split(",");
    const long = point.split(", ");
    const coord = long.map(Number);

    //create rest of variables
    const fod_type = obj.fod_type;
    const timestamp = obj.timestamp;
    const recommended_action = obj.recommended_action;
    const uuid = obj.uuid;

    //create marker
    const marker = new L.marker(coord).addTo(this.map);
    const custom_style = {
      maxWidth: 220,
      minWidth: 160,
      closeOnClick: false,
      className: `log-popup`,
    };
    const content = `
            <h2>Type: ${fod_type}</h2> 
            <p> Coords: [${coord}]</p>
            <p> Time: ${timestamp}</p>
            <p> recommended cleanup action: ${recommended_action}</p>
            <img height=150 width =150 src="http://127.0.0.1:8000/fod_img/${uuid}"> 
        `;
    marker.bindPopup(content, custom_style);

    // remove on double click
    marker.on("dblclick", () => {
      this.map.removeLayer(marker);
      fetch(
        "http://127.0.0.1:8000/mark_clean/" +
          new URLSearchParams({
            uuid,
          }),
        { method: "PATCH" }
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        });
    });
    //Verify delete: "Are you sure you want to delete?"
    //add button and show details + images
  }
  radius = async function () {
    try {
      const data = fetch("http://127.0.0.1:8000/common_location");
      const res = await Promise.race([data, this._timeout(TIMEOUT_SEC)]);
      const dataRes = await res.json();

      dataRes.split(",");
      const long = dataRes.split(", ");
      const coord = long.map(Number);

      //add radius to map
      var circle = L.circle(coord, {
        color: "lightred",
        fillColor: "#f03",
        fillOpacity: 0.5,
        radius: 100,
      }).addTo(this.map);

      if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
    } catch (err) {
      throw err;
    }
  };
}

var map = new Map();
map.__addAllUnclean();

function renderLog(data) {
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
    </div>  <div class="object_row">
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

function notification() {
  var audio = new Audio("../static/mixkit-long-pop-2358.wav");
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
  toggleFeed();
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
  sideNotif.style.display = "none";
  radiusbtn.style.display = "none";
  feedbtn.style.display = "none";
}
function closeNav() {
  sidePanel.style.width = "0";
  mySidepanel.style.display = "block";
  sideCam.style.display = "block";
  form.style.display = "block";
  sideNotif.style.display = "block";
  radiusbtn.style.display = "block";
  feedbtn.style.display = "block";
}

var vid_enabled = false;
function toggleFeed() {
  if (vid_enabled) {
    var video_feed = document.getElementById("video_feed");
    showVideo.removeChild(video_feed);
    vid_enabled = false;
  } else {
    img_tag = `<img id="video_feed" src="http://127.0.0.1:8000/video_feed" width="50%"></img>`;
    showVideo.insertAdjacentHTML("afterbegin", img_tag);
    vid_enabled = true;
  }
}
