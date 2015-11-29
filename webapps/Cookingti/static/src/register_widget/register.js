$(document).ready(function()
{
	$("#register_barcode_show").click(function()
	{
		$("#register_barcode_panel").show(200);
		$("#register_mask").show(200);
		
		return false;
	});
	
	$("#register_upload_barcode_cancel").click(function()
	{
		$("#register_barcode_panel").hide(200);
		$("#register_mask").hide(200);
	});
});