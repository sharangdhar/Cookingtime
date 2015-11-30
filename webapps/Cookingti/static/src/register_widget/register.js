$(document).ready(function()
{
	
    // CSRF set-up copied from Django docs
    function getCookie(name) {  
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });
	
	
	
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
	
	
	$("#register_upload_barcode_submit").click(register_barcode_submit);
	
});

function register_barcode_submit(e)
{
	var fd = new FormData();
	fd.append('picture', $("#register_upload_barcode_file")[0].files[0]);
	

	
	$.ajax(
	{
        url: '/barcode_image',
        data: fd,
        processData: false,
		contentType: false,
        type: 'POST',
        success: function (data) 
		{
			console.log(data);
		},
		error: function(data, textStatus, errorThrown)
		{
			console.log(data, textStatus, errorThrown);
		}
	});
}

