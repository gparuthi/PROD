// beginning of the UI methods
var WEBSOCKET_SERVER_URL = "ws://localhost:9000";//"ws://dhcp3-173.si.umich.edu:9000";
 var _nextX=0;
 var _nextY=0;
 
 function resetXY()
 {
 	_nextX=0;
 	_nextY=0;
 };
 
 function updateXY(width,height)
 {
 	MAX_X = window.screen.width;
 	MAX_Y = window.screen.height;
 	 
 	if(_nextX + width >MAX_X)
 	{
 		_nextX=0;
 		_nextY= _nextY+height;
 	}else
 	{
 		_nextX = _nextX+width;
 	}
 	//console.log(_nextX + ":" + _nextY);
 }
 function init(id, width, height)
 {
 	var currentX = _nextX;
 	var currentY= _nextY;
 	
 	var framewidth = width + 5;
 	var frameheight = height + 5;
	
  	updateXY(width,height);
 	
     canvas = document.getElementById("testCanvas");
		stage = new Stage(canvas);

		var container = new Container();
		stage.addChild(container);
		
		//console.log("id:"+id);
		
		var content = new DOMElement(id);
		content.regX = 5;
		content.regY = 5;
		//content.visible = false;

		var o = content.clone();
		stage.addChild(o);

		container.addChild(content);
		container.x = currentX+5; container.y = currentY+5;
		//container.alpha = 0.6;
		//container.rotation = 25;
		//container.scaleX = 1.5;
		//container.visible = false;

		stage.update();
 }

//Ending of the UI methods

//Beginning of the socket methods

var sock = null;
var ellog = null;
var idno =0;

window.onload = function() {

    ellog = document.getElementById('log');

    var wsuri;
    if (window.location.protocol === "file:") {
	wsuri = WEBSOCKET_SERVER_URL;
    } else {
	wsuri = "ws://" + window.location.hostname + ":9000";
    }

    if ("WebSocket" in window) {
	sock = new WebSocket(wsuri);
    } else if ("MozWebSocket" in window) {
	sock = new MozWebSocket(wsuri);
    } else {
	log("Browser does not support WebSocket!");
	window.location = "http://autobahn.ws/unsupportedbrowser";
    }

    if (sock) {
	sock.onopen = function() {
	    //	    log("Connected to " + wsuri);
	}

	sock.onclose = function(e) {
	    // log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
	    sock = null;
	}

	sock.onmessage = function(e) {
	    log(e.data);
	}
    }
};

function send() {
    var msg = document.getElementById('message').value;
    if (sock) {
	sock.send(msg);
	log("Sent: " + msg);
    } else {
	log("Not connected.");
    }
};
function sendTwitter() {
    var msg = "<iframe frameborder=0 height=330 scrolling=no src=gadgets/twitter_search.html width=335></iframe>";
    if (sock) {
	sock.send(msg);
	log("Sent: " + msg);
    } else {
	log("Not connected.");
    }
};
function log(m) {
    //ellog.innerHTML += m + '\n';
    //ellog.scrollTop = ellog.scrollHeight;
    m = trim1(m);
    //console.log(m);
    if(m=='RESET')
    {
    	//console.log("Resetting the view..");
    	//remove all existing ids
    	RemoveExistingIds();
    	//reset the UI xy positions
    	resetXY();
   	}
   	else
   	{
	 
		m = "<iframe frameborder=0 height=330 width=335 scrolling=no src=" + m + "></script>";

		idno = idno + 1;
		var id = getId(idno);

		var css_link = $("<link>", {
			rel : "stylesheet",
			type : "text/css",
			href : "style.css"
		});
		css_link.appendTo('head');
		//element = "<div>"+m+"</div>";
		//		ellog.innerHTML += element +'\n';


		element = "<div class='widgets' style='display:none;' id='" + id + "'>" + m + "</div>";
		$('#e').append(element);

		elediv = document.getElementById(id);

		$(elediv).fadeIn(3000);

		init(id, 250, 300);
	}

		
};
function RemoveExistingIds()
{
	$('.widgets').fadeOut(1000);
	$('.widgets').remove();
	idno =0;
	
};

function getId(idno)
{
	return 'id'+idno;
};

function trim1 (str) {
    return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '').replace(/'/g, '');
}