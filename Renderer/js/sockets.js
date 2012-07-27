      var sock = null;
var ellog = null;
var idno =0;

window.onload = function() {

    ellog = document.getElementById('log');

    var wsuri;
    if (window.location.protocol === "file:") {
	wsuri = "ws://localhost:9000";
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
	 m = "<iframe frameborder=0 height=330 width=335 scrolling=no src=" +m + "></script>";
        
      idno = idno+1;
      var id = 'id'+idno;
       
            var css_link = $("<link>", {
		    rel: "stylesheet",
		    type: "text/css",
		    href: "style.css"
		});
		css_link.appendTo('head');
		//element = "<div>"+m+"</div>";
		//		ellog.innerHTML += element +'\n';

		
		console.log(id);

		element = "<div style='display:none;' id='"+id+"'>"+m+"</div>";
		$('#e').append(element);
		
		elediv = document.getElementById(id);

		$(elediv).fadeIn(3000);
		
		init(id,250,300);
		
};
     