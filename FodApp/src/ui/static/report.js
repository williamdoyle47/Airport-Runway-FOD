const mySidepanel = document.querySelector(".openbtn");
const foddCount = document.querySelector(".fodCount");
const unCleanFodCount = document.querySelector(".unCleanfodCount");
const fodtype = document.querySelector(".fodtype");
const fodCoord = document.querySelector(".fodCoord");
const fodCleanup = document.querySelector(".fodcleanup");
const typeResults = document.querySelector(".typeResults");
const sidePanel = document.getElementById("mySidepanel");

const TIMEOUT_SEC = 10;

// fetch and display data

function timeout(s) {
  return new Promise(function (_, reject) {
    setTimeout(function () {
      reject(new Error(`Request took too long! Timeout after ${s} second`));
    }, s * 1000);
  });
}
async function fodCount() {
  try {
    const data = fetch("http://127.0.0.1:8000/all_logs");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    const fodCount = dataRes.length;

    foddCount.innerHTML = fodCount;

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}
//generate fod file

async function generateCSV() {
  try {
    const data = fetch("http://127.0.0.1:8000/generate_csv");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    alert(`CSV successfully created!`);
    console.log("CSV successfully created!");

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}
function renderTable(data) {
  var tbodyRef = document
    .getElementById("resultsTable")
    .getElementsByTagName("tbody")[0];
  var newRow = tbodyRef.insertRow();

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.uuid);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.fod_type);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.coord);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.recommended_action);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.timestamp.split("T")[0]);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(data.timestamp.split("T")[1]);
  newCell.appendChild(newText);

  var newCell = newRow.insertCell();
  var newText = document.createTextNode(
    `${data.cleaned_timestamp ? data.cleaned_timestamp : "N/A"}`
  );
  newCell.appendChild(newText);
}

// this is obv not ideal code as we repeat ourselves for every each class of FOD -- fix later
async function nut(fodType) {
  try {
    var dateControl = document.querySelector('input[type="date"]');

    console.log(dateControl.value);
    const data = fetch("http://127.0.0.1:8000/all_logs");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    var topCount; //leave as var as it will be redefined
    var dataRes = await res.json();

    if (dateControl.value) {
      dataRes = dataRes.filter(
        (fod) => fod.timestamp.split("T")[0] === dateControl.value
      );
      console.log("Filtering by date...");
    }

    if (fodType == "all") {
      topCount = dataRes.slice(0, 40);
    }

    if (fodType == "nut") {
      var fod = dataRes.filter((nut) => nut.fod_type === "nut");
      // var fod = dataRes.filter((nut) => nut.fod_type === "nut");
      //filter by date value
      topCount = fod.slice(0, 20);
    }

    if (fodType == "bolt") {
      const fod = dataRes.filter((nut) => nut.fod_type === "bolt");
      topCount = fod.slice(0, 20);
    }

    if (fodType == "wrench") {
      const fod = dataRes.filter((nut) => nut.fod_type === "wrench");
      topCount = fod.slice(0, 20);
    }

    if (fodType == "concrete") {
      const fod = dataRes.filter((nut) => nut.fod_type === "concrete");
      topCount = fod.slice(0, 20);
    }
    if (fodType == "pliers") {
      const fod = dataRes.filter((nut) => nut.fod_type === "pliers");
      topCount = fod.slice(0, 20);
    }
    if (fodType == "screwdriver") {
      const fod = dataRes.filter((nut) => nut.fod_type === "screwdriver");
      topCount = fod.slice(0, 20);
    }
    if (fodType == "wood") {
      const fod = dataRes.filter((nut) => nut.fod_type === "wood");
      topCount = fod.slice(0, 20);
    }

    var tbodyRef = document
      .getElementById("resultsTable")
      .getElementsByTagName("tbody")[0];

    var new_tbody = document.createElement("tbody");

    tbodyRef.parentNode.replaceChild(new_tbody, tbodyRef);

    var FODcountperclass = document.getElementById("FODcountperclass");

    FODcountperclass.innerHTML = topCount.length;

    new_tbody.setAttribute("id", "resultsTableBody");

    topCount.forEach((fodtp) => {
      renderTable(fodtp);
    });

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}
async function commonFod() {
  try {
    const data = fetch("http://127.0.0.1:8000/common_fod_type");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    fodtype.innerHTML = dataRes;

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}

async function avgCleanUpTime() {
  try {
    const data = fetch("http://127.0.0.1:8000/avg_cleanup_time");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    console.log(dataRes);
    fodCleanup.innerHTML = dataRes;

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}

async function commonLocation() {
  try {
    const data = fetch("http://127.0.0.1:8000/common_location");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    console.log(dataRes);
    fodCoord.innerHTML = dataRes;

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}

async function totalUncleanFod() {
  try {
    const data = fetch("http://127.0.0.1:8000/total_unclean");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();
    console.log(dataRes);
    unCleanFodCount.innerHTML = dataRes;

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}

//Generate anaylysis

function generateAnalysis() {
  fodCount();
  totalUncleanFod();
  commonFod();
  commonLocation();
  avgCleanUpTime();
}
//Display Functions

function openNav() {
  sidePanel.style.width = "250px";
  mySidepanel.style.display = "none";
}
function closeNav() {
  sidePanel.style.width = "0";
  mySidepanel.style.display = "block";
}

function openNav() {
  sidePanel.style.width = "250px";
  mySidepanel.style.display = "none";
}
function closeNav() {
  sidePanel.style.width = "0";
  mySidepanel.style.display = "block";
}

// Get the modal
const modal = document.getElementById("myModal");

// Get the button that opens the modal
const btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

window.onload = () => {
  //FILE READER + HTML ELEMENTS

  var reader = new FileReader(),
    picker = document.getElementById("picker"),
    tablecsv = document.getElementById("tablecsv");

  //Read CSV on file pick
  picker.onchange = () => reader.readAsText(picker.files[0]);

  // Read the csv file & generate HTML
  reader.onloadend = () => {
    let csv = reader.result;
    console.log(csv);

    tablecsv.innerHTML = "";

    let rows = csv.split("\r\n");

    //loop through
    for (let row of rows) {
      let cols = row.match(/(?:\"([^\"]*(?:\"\"[^\"]*)*)\")|([^\",]+)/g);
      console.log(cols);
      if (cols != null) {
        let tr = tablecsv.insertRow();
        for (let col of cols) {
          let td = tr.insertCell();
          td.innerHTML = col;
        }
      }
    }
  };
};
