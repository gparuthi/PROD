var stage;

	function init() {
		// create a new stage and point it at our canvas:
		canvas = document.getElementById("testCanvas");
		stage = new createjs.Stage(canvas);

		var container = new createjs.Container();
		stage.addChild(container);

		var frame = new createjs.Shape();
		frame.graphics.beginFill("#00F").drawRect(0,0,340,280);
		frame.regX = 170;
		frame.regY = 140;

		var content = new createjs.DOMElement("e");
		content.regX = 165;
		content.regY = 135;
		//content.visible = false;

		var o = content.clone();
		stage.addChild(o);

		container.addChild(frame,content);
		container.x = 300; container.y = 200;
		container.alpha = 0.6;
		container.rotation = 25;
		container.scaleX = 1.5;
		//container.visible = false;

		stage.update();
	}