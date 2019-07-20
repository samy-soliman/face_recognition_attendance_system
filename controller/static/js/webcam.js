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
  if(img_count!=100){
    $(document).ready( function(){
      $("#messageDiv5").html(img_count).show('fast');
    });
  img_count = img_count +1;
  videoImageToDataURL();
  }
  
  else{
    $(document).ready( function(){
      $("#messageDiv5").addClass('alert alert-success').removeClass('alert alert-danger').html("Done").delay(1500).fadeOut('fast');
    });

    var myform = document.getElementById('studentAddForm')
    var hiddenInput = document.getElementById('studentPhotos')

    hiddenInput.value = JSON.stringify(dataUrls)

    myform.appendChild(hiddenInput)
    
    clearInterval(interval_ID)
    closeWebCam();
  }
}

function startImageHandler(){
  interval_ID = setInterval(handleLogic, 250);
}


