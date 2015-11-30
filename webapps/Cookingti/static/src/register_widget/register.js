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
			if(data.status == "success")
			{
				$("#register_barcode").val(data.data.barcode);
				get_wattage(data.data.barcode);
			}
			else
			{
				var error = $("#register_upload_barcode_error");
				if(data.custom_errors)
				{
					error.text(error.text() + " " + data.custom_errors[0].message);
				}
				
				if(data.errors)
				{
					if(data.errors.picture)
					{
						error.text(errror.text()  + " " +  data.errors.picture.join(', '));
					}
				}
			}
		},
		error: function(data, textStatus, errorThrown)
		{
			console.log(data, textStatus, errorThrown);
			$("#register_upload_barcode_error").text(errorThrown);
		}
	});
}

function get_wattage(barcode)
{
	$.post("/lookup_wattage", {barcode:barcode}).done(function(data)
	{
		if(data.status == "success")
		{
			$("#id_wattage").val(data.data.wattage);
			
			$("#register_barcode_panel").hide(200);
			$("#register_mask").hide(200);
		}
		else
		{

			var error = $("#register_upload_barcode_error");
			
			if(data.custom_errors)
			{
				error.text(error.text() + " " + data.custom_errors[0].message);
			}
		
			
			
			return false;
		}
	}).fail(function()
	{
		console.log(data, textStatus, errorThrown);
		$("#register_upload_barcode_error").text(errorThrown);
	
		return false;
	});
}