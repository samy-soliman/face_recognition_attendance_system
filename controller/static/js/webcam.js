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

var img_count = 0;
var interval_ID;
var dataUrls = [];


function videoImageToDataURL(refreshIntervalId){
  var video = document.querySelector('video');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');

  context.drawImage(video,0,0,400,300);
  var dataURL = canvas.toDataURL('image/png');

  dataUrls.push(dataURL);

}

function handleLogic(){
  if(img_count!=20){
    if (img_count%10 ==0)
    {
      // test
      alert(img_count);
    }
  img_count = img_count +1;
  videoImageToDataURL();
  }
  else{
    var myform = document.getElementById('studentAddForm')
    var hiddenInput = document.createElement('input')

    hiddenInput.type = 'hidden'
    hiddenInput.name = 'dataUrls'
    hiddenInput.value = JSON.stringify(dataUrls)

    myform.appendChild(hiddenInput)
    
    clearInterval(interval_ID)
    closeWebCam();

    window.alert('photos has been taken')

  }
}

function startImageHandler(){
  interval_ID = setInterval(handleLogic, 500);
}


