function closeWebCam(){
    var video = document.querySelector('video');
    video.pause();
    const tracks = media.getTracks()
    tracks.forEach(track => {
      track.stop();
    });
}


function start(){
  // Prefer camera resolution nearest to 1280x720.
  var constraints = { audio: true, video: { width: 1280, height: 720 } }; 
  
  navigator.mediaDevices.getUserMedia(constraints)
  .then(function(mediaStream) {
    var video = document.querySelector('video');
    media = mediaStream
    video.srcObject = mediaStream;
    video.onloadedmetadata = function(e) {
      video.autoplay=false
      video.play();
    };
  })
  .catch(function(err) { console.log(err.name + ": " + err.message); }); // always check for errors at the end.
}

var dataURL;
function videoImageToDataURL(){
  var video = document.querySelector('video');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');

  context.drawImage(video,0,0,400,300);
  dataURL = canvas.toDataURL('image/png');

}

function sendPhoto(){

    videoImageToDataURL();

    var myform = document.getElementById('attendanceForm')
    var hiddenInput = document.createElement('input')

    hiddenInput.type = 'hidden'
    hiddenInput.name = 'dataURL'
    hiddenInput.value = JSON.stringify(dataURL)

    myform.appendChild(hiddenInput)
    
    closeWebCam();

    window.alert('photo has been taken')
}
