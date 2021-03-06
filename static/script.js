var up = false;
var right = false;
var down = false;
var left = false;
var cam_up = false;
var cam_down = false;

var lock = false;
var turn = 7.5;
var camera_pos = 10;

document.addEventListener('keydown',press);

function press(e){
    lock = false;
    if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */){
	up = true;
    }
    if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
	right = true
    }
    if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
	down = true
    }
    if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */){
	left = true
    }
    if (e.keyCode === 90) /* z */
    {
	cam_down = true;
    }
    if (e.keyCode === 81) /* q */
    {
	cam_up = true;
    }
}

document.addEventListener('keyup',release);

function release(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    up = false
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    right = false
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    down = false
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */){
      left = false
  }
  if (e.keyCode === 90) /* z */{
      cam_down = false;
  }
  if (e.keyCode === 81) /* q */{
      cam_up = false;
  }
};

var responce = function(responce, status){
    console.log(responce, status);
}

var post_function = function(command, data){
    //$.post("api/car/forward", {duration: 1, speed: 30}, function(result){
        //console.log(result);
    //});

    url_str = '/'
    data_cmd = null
    
    switch(command){
    case 'forward':
	url_str = "/api/car/forward";
	data_cmd = {duration: 2, speed: 30}
	break;
    case 'backward':
	url_str = "/api/car/backward";
	data_cmd = {duration: 2, speed: 30}
	break;
    case 'left':
	url_str = "/api/car/turn";
	data_cmd = {degree: turn-=0.5}
	console.log('lf', data_cmd)
	break;
    case 'right':
	url_str = "/api/car/turn";
	data_cmd = {degree: turn+=0.5}
	console.log('lf', data_cmd)
	break;
    case 'camera_up':
	url_str = "/api/car/cam_position";
	camera_pos += 1;
	console.log('position', camera_pos)
	data_cmd = {position: camera_pos}
	break;
    case 'camera_down':
	url_str = "/api/car/cam_position";
	camera_pos -= 1;
	console.log('position', camera_pos)
	data_cmd = {position: camera_pos}
	break;
	
	
    }

    $.ajax({
        type : "POST",
        url : url_str,
        contentType : "application/json",
        data : JSON.stringify({data : data_cmd}),
        dataType: "json",
        async: false,
        success: function(data) {
            console.log("success: " + data);
        }
    });
    
    
    //$.post("api/car/forward", {duration: 1, speed: 30}, responce); 
    //console.log('hehehe');
}

function gameLoop(){
    if (lock != true ){
	if(up){
	    lock = true;
	    post_function('forward', '---');
            console.log('up');
	}
	if(down){
            lock = true;
	    post_function('backward', '---');
	    console.log('down');
	}
	if(left){
	    lock = true;
	    post_function('left', '---');
	    console.log('left');
	}
	if(right){
	    lock = true;
	    post_function('right', '---');
	    console.log('right');
	}
	if(cam_up){
	    lock = true;
	    post_function('camera_up', '---');
	    console.log('cam_up');
	}
	if(cam_down){
	    lock = true;
	    post_function('camera_down', '---');
	    console.log('cam_down');
	}
    }
    window.requestAnimationFrame(gameLoop)
};

window.requestAnimationFrame(gameLoop);
