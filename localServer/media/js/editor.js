$(document).ready(function(){
	$("#addSpeaker").click(function(){
		$(".speakers").append('<input type="text" name="speaker[]" placeholder="palestrante"> <br>');
		return false;
	});
	$("#addPainelist").click(function(){
		$(".painelists").append('<input type="text" name="painelist[]" placeholder="painelista"> <br>');
		return false;
	});
	if(notTime !== undefined){
		$(".values").html("");
		for(var i = 0; i < $("#days").val(); i++){
			$(".values").append('<input type="text" name="time['+i+']">');
		}
	}
	$("#time-close").click(function(){
		$(".block").fadeOut();
	});
	$("#open-time").click(function(){
		$(".block").fadeIn();
	});
});