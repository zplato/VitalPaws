function isDeviceMotionSupported() {
    return 'DeviceMotionEvent' in window;
}


function isPermissionRequired() {
    return 'requestPermission' in DeviceMotionEvent;
}





function beginMotionDetection(motionHandler) {
    if ('DeviceMotionEvent' in window) {
        console.log('Motion Detection Started')
        window.addEventListener('devicemotion', motionHandler, false);
    } 
}

function endMotionDetection(motionHandler) {
    console.log('Motion Detection Stopped')

    window.removeEventListener('devicemotion', motionHandler, false);
}

// function accelerationHandler(acceleration) {
//     var info, xyz = "[X, Y, Z]";

//     info = xyz.replace("X", acceleration.x && acceleration.x.toFixed(3));
//     info = info.replace("Y", acceleration.y && acceleration.y.toFixed(3));
//     info = info.replace("Z", acceleration.z && acceleration.z.toFixed(3));
// }


export { isDeviceMotionSupported, isPermissionRequired, beginMotionDetection, endMotionDetection};
