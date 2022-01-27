if ("webkitSpeechRecognition" in window) {
  let speechRecognition = new webkitSpeechRecognition();
  let final_transcript = "";

  speechRecognition.continuous = true;
  speechRecognition.interimResults = false;
  speechRecognition.lang = 'en-US'

  speechRecognition.onresult = function(event){

    for (let i = event.resultIndex; i < event.results.length; ++i) {
        final_transcript += event.results[i][0].transcript;
    }
    final_transcript +='. ';
    document.getElementById('newLog').value = final_transcript;
  };
 
  function startRecording(){
    speechRecognition.start();
    document.getElementById('Recording').innerHTML = '<button class="btn btn-danger" id="stop" onclick = stopRecording()><i class="bi bi-mic-mute-fill"></i> Stop Recording</button>'
  }

  function stopRecording(){
    speechRecognition.stop();
    document.getElementById('Recording').innerHTML = '<button class="btn btn-success" id="stop" onclick = startRecording()><i class="bi bi-mic-fill"></i> Start Recording</button>'
  }
} else {
  console.log("Speech Recognition Not Available");
}
