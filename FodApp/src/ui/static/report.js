const mySidepanel = document.querySelector(".openbtn");
const foddCount = document.querySelector(".fodCount");
const fodtype = document.querySelector(".fodtype");
const fodCoord = document.querySelector(".fodCoord");
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
    console.log("CSV successfully created!");

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}
function renderTable(data) {
  const html = `
  <table>
    <tr>
      <td>${data.id}</td>
      <td>${data.fod_type}</td>
      <td>${data.coord}</td>
      <td>${data.recommended_action}</td>
      <td>${data.timestamp.split("T")[0]}</td>
      <td>Details...</td>
    </tr> 
  </table>
  `;
  typeResults.insertAdjacentHTML("beforeend", html);
}
async function nut() {
  try {
    const data = fetch("http://127.0.0.1:8000/all_logs");
    const res = await Promise.race([data, timeout(TIMEOUT_SEC)]);
    const dataRes = await res.json();

    //filter the 'Nut'
    const nut = dataRes.filter((nut) => nut.fod_type === "nut");
    const topfive = nut.slice(0, 5);
    console.log(topfive);
    topfive.forEach((fodtp) => {
      console.log(fodtp);
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

    /*
    //Show most common fod

    let mostFreq = 1;
    let count = 0;
    let commonFod;

    for (let i = 0; i < dataRes.length; i++) {
      for (let j = i; j < dataRes.length; j++) {
        if (dataRes[i] == dataRes[j]) count++;
        if (mostFreq < count) {
          mostFreq = count;
          commonFod = dataRes[i];
          fodtype.innerHTML = commonFod;
          console.log(commonFod, count);
        }
      }
      count = 0;
    }
    console.log(commonFod);
    */

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

    /*
    //Show most common coord

    let mostFreq = 1;
    let count = 0;
    let coordLocal;

    for (let i = 0; i < dataRes.length; i++) {
      for (let j = i; j < dataRes.length; j++) {
        if (dataRes[i] == dataRes[j]) count++;
        if (mostFreq < count) {
          mostFreq = count;
          coordLocal = dataRes[i];
          fodCoord.innerHTML = coordLocal;
          console.log(coordLocal, count);
        }
      }
      count = 0;
    }
    console.log(coordLocal);
    */

    if (!res.ok) throw new Error(`cannot reach url ${res.status}`);
  } catch (err) {
    throw err;
  }
}

//Generate anaylysis

function generateAnalysis() {
  fodCount();
  commonFod();
  commonLocation();
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
