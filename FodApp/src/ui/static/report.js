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
