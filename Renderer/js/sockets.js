// beginning of the UI methods
var WEBSOCKET_SERVER_URL = "ws://dhcp3-173.si.umich.edu:9000";// "ws://localhost:9000";//"ws://dhcp3-173.si.umich.edu:9000";
MAX_X = window.screen.width;
MAX_Y = window.screen.height;
 var _nextX=0;
 var _nextY=0;
 
 function resetXY()
 {
 	_nextX=0;
 	_nextY=0;
 };
 
 function updateXY(width,height)
 {
 	
 	 
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
		coords = getCoordinates(id,width,height);
		
		container.x = coords.X;
		container.y = coords.Y;
		
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
	
	// read and convert the input to json
	m = m.substr(m.indexOf('{'),m.indexOf('}'))
	//console.log(m)
	var a =	jQuery.parseJSON(m);
	// a loooks likes {"src": "gadgets/flickr_tags.html?ids=cats,dogs", "h": 400, "id": "id2", "w": 300, "f": "A"} 
	id = a['id'];
    if(a['f']=='R')
    {
    	// R is for removing the id element
    	console.log('Removing ' + id)
    	RemoveIds(id);
    	//reset the UI xy positions
    	//resetXY();
   	}
   	else 
   	//if (a['f'=='A'])
   	{
		// Add the element to the div
		src = "<iframe frameborder=0 height=330 width=335 scrolling=no src=" + a['src'] + "></script>";
/*
		var css_link = $("<link>", {
			rel : "stylesheet",
			type : "text/css",
			href : "style.css"
		});
		css_link.appendTo('head');
	*/	
		element = "<div class='widgets' style='display:none;' id='" + id + "'>" + src + "</div>";
		$('#e').append(element);

		elediv = document.getElementById(id);

		$(elediv).fadeIn(3000);

		init(id, a['w'], a['h']);
	}

		
};
// create a matrix describing the screen space
// each node is about 300x300 (about one widget) 
var a = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]];
var id_co_dict = [];

function getCoordinates(id, width, height)
{
	x=0;
	y=0;
	res = a[y][x];
	count=0;
	while (a[y][x] == 1 && count <10)
	{
		// randomly select a square and check if its empty (0)
		x = Math.floor(Math.random()*(4));
		y = Math.floor(Math.random()*(3));
		count++;
	}		
//	console.log(x+" "+ y)
	a[y][x] = 1
	id_co_dict[id]=[];
	id_co_dict[id].x = x;
	id_co_dict[id].y = y;
	
	var ret = [];
	//randomly find some area around this square
	ret.X = Math.floor(Math.random()*(100)) + x*300;
	ret.Y = Math.floor(Math.random()*(100)) + y*200;
	
	console.log (ret.X + " " + ret.Y);
	return ret
}

function RemoveIds(id)
{
	if($('#' + id).length != 0)
	{
		$('#'+id).fadeOut(4000, function(){$('#'+id).remove();});
		
		
		a[id_co_dict[id].y][id_co_dict[id].x] = 0;
	}
}
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