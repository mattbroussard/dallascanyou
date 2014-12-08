
(function() {
	
	var phrases = [
		"take out the trash",
		"turn off the lights",
		"do my homework",
		"order me a pizza",
		"make me a sandwich",
		"turn on the TV",
		"pick me up at work",
		"get my laptop charger",
		"carry me to class"
	];

	var phraseIndex = 0;
	var charIndex = 0;
	var animating = true;
	var animStep = 1;
	var updateTimeout = null;

	// shuffle phrases
	for (var i = 0; i < phrases.length; ++i) {
		var j = Math.round(Math.random()*(phrases.length-1));
		var tmp = phrases[j];
		phrases[j] = phrases[i];
		phrases[i] = tmp;
	}

	var updateAnimation = function() {
		if (!animating) return;

		var str = phrases[phraseIndex];
		var len = str.length;

		if (charIndex + animStep < 0) {
			animStep = 1;
			charIndex = 0;
			phraseIndex = (phraseIndex + 1) % phrases.length;
		} else if (charIndex + animStep > len) {
			animStep = -2;
		} else {
			charIndex += animStep;
			$("#entry").val(str.substring(0, charIndex));
		}

		startAnimation();

	};

	var startAnimation = function() {
		var time = animStep > 0 ? 35 : 10;
		if (animStep == -2) {
			time = 200;
			animStep = -1;
		}
		updateTimeout = setTimeout(updateAnimation, Math.round(Math.random()*50) + time);
	};

	var focus = function() {
		if (animating) {
			animating = false;
			clearTimeout(updateTimeout);
			$("#entry").val("");
		}
	};

	var unfocus = function() {
		if ($("#entry").val() == "") {
			animating = true;
			phraseIndex = 0;
			charIndex = 0;
			startAnimation();
		}
	};

	$(function() {
		$("#entry").bind("focus", focus).bind("blur", unfocus);
		startAnimation();
	});

})();