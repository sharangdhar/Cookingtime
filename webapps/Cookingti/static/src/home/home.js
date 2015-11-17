$(document).ready(function()
{
	var TIME = 200;
	
	$("#latest_heading").click(function(e)
	{
		$("#highest").hide(TIME);
		$("#latest").show(TIME);
			
		$("#highest_heading").removeClass("hs_title_selected");
		$("#latest_heading").addClass("hs_title_selected");
	});
	
	$("#highest_heading").click(function(e)
	{
		$("#latest").hide(TIME);
		$("#highest").show(TIME);
		
		$("#latest_heading").removeClass("hs_title_selected");
		$("#highest_heading").addClass("hs_title_selected");
	});
});