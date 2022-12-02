'use strict';

// const camera1 = document.getElementById('camera1');
// const camera2 = document.getElementById('camera2');

// const cleanUp = (whichCamera) => {
//     try{
//         const stream = camera1.srcObject;
//         const tracks = stream.getTracks();
//         tracks.array.forEach(track => {
//             track.stop()
//         });
//     } catch(error){
//         console.log(error);
//     }
// }

// cleanUp(camera1);
// cleanUp(camera2);

const myVideoInputs = [];
const doGetDevicesInfo = async () => {
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

const startCamera = async (myVideoInput, whichCamera) => {
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

const doStartCamera = (button) => {
    const id = button.id;
    switch(id){
        case 'startCamera1':
            startCamera(myVideoInputs[1], camera1);
            break; 
        case 'startCamera2':
            startCamera(myVideoInputs[2], camera2);
            break; 
    }
}