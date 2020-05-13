let model, webcam, ctx, maxPredictions;

// The type of exercice : 0 = SEQUENTIAL ; 1 = SINGLE POSITION TO MAINTAIN

// Name of the exercice and its AI's path
const URL = "/static/" + name + "/";

// If counter >= value --> Change exercice 
var counter = 0;
var value = Math.trunc(value);

// For MODE 0:
var sequence = [];
var index = 0;

// For MODE 1:
var malus = 0;
var timer = 0;
var startTime = 0;
var lastT = 0;

// Should stop program
var stop = false;


// Initialize the program
async function init() {
    // Load the models
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";
    model = await tmPose.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    // Setup the camera feed
    const size = 500;
    const flip = true;
    webcam = new tmPose.Webcam(size, size, flip);
    await webcam.setup();
    await webcam.play();

    // Init the loop!
    window.requestAnimationFrame(loop);
    
    // Attach the camera feed to the canvas
    const canvas = document.getElementById("canvas");
    canvas.width = size; canvas.height = size;

    // Setup the 2D context
    ctx = canvas.getContext("2d");
    
    // Init the scoring
    if(type == 0)
        document.getElementById("n").innerHTML = name + " : 0/" + value + "!";
    else if(type == 1)
        document.getElementById("n").innerHTML = name + " : " + "0/" + value + " s !"
}

// The loop : Update the webcam, predict and recursion
async function loop(timestamp) { 
    webcam.update(); 
    await predict().catch((e) => {});
    window.requestAnimationFrame(loop);
}

async function predict() {

    // Get AI's output.
    const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
    const prediction = await model.predict(posenetOutput)
        
    // Count the number of reps (no timing for each rep)
    if(type == 0){

        // create the sequence of positions
        if(sequence.length == 0){
            for(var i = 0; i < prediction.length-1; i++){
                sequence.push(i);
            }
            for(var i = prediction.length - 3; i >= 0; i--){
                sequence.push(i);
            }
            console.warn(sequence);
        }    

        // While the sequence is not empty, we try to go through. And each cycle we update the counter.
        if(sequence.length != 0){
            
            if(prediction[sequence[index]].probability.toFixed(2) >= 0.95){
                console.warn(sequence[index]);
                
                if(index < sequence.length-1){
                    index += 1;
                }else {
                    index = 0;
                    counter += 1;
                    document.getElementById("n").innerHTML = name + " :" + counter + "/" + value  + "!"
                }
            }

        }
    
    // Times the pos asked (only one here). Deducts time if the pos is not maintained.
    }else if(type == 1){
        var currentT = new Date();        
        if(prediction[0].probability.toFixed(2) >= 0.80){  
            timer += (currentT - lastT)/1000;
        }else if(timer > 0){
            timer -= (currentT - lastT)/1000;
            if(timer < 0)
                timer = 0;
        }
        document.getElementById("n").innerHTML = name + " : " + timer.toFixed(2) + "/" + value + " s !"
        lastT = currentT;
    }

    // If the exercice if DONE : Send request to the server
    if((timer >= value || counter >= value) && stop == false){
        document.getElementById("n").style = "color:#0F0;"
        stop = true;
        // document.getElementById("canvas").hidden = true;
        var request = $.ajax({
            url: "/process",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                pushups : value
                }),  
            })  
            .done( function (request) {
            })
        if(isLast == 0){
            setTimeout(() => {location.reload()}, 1000)
        }
    }
    
    // Draw
    drawPose(pose);
}


// Draw the position detected by the AI
function drawPose(pose) {
    if (webcam.canvas) {
        ctx.drawImage(webcam.canvas, 0, 0);
        if (pose) {
            const minPartConfidence = 0.5;
            tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
            tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
        }
    }
}

// Certificate
var csrftoken = $('meta[name=csrf-token]').attr('content')
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

init();