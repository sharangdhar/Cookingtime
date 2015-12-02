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
	
	
	
	$("#new_button_barcode_button").click(function()
	{
		$("#new_item_barcode_wrapper").toggle(200);
	});
	
	$("#barcode_submit").click(new_item_barcode_submit);
});


function new_item_barcode_submit(e)
{
	$("#barcode_new_response").text("");
	
	var fd = new FormData();
	fd.append('picture', $("#barcode_image")[0].files[0]);
	
	var barcode = "";
	var barcode_type = "";
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
				barcode = data.data.barcode;
				barcode_type = data.data.type;
				
				var item_type = $('#barcode_new_type').val();
				$.post("/new_by_barcode", {barcode:barcode, barcode_type:barcode_type, item_type:item_type}).done(function(data)
				{
					if(data.status == "success")
					{
						$("#barcode_new_response").text("Success!");
						addr = "/item/" + item_type + "/" + data.id;
						window.location = addr;
					}
					else
					{
						var error = $("#barcode_new_response");
						
						if(data.exists)
						{
							$("#barcode_new_response").text("Item exists. Redirecting...");
							addr = "/item/" + item_type  + "/" +  data.exists;
							setTimeout(function(){window.location = addr;}, 5000);
							return;
						}
						if(data.custom_errors)
						{
							error.text(error.text() + " " + data.custom_errors[0].message);
						}
						
						if(data.errors)
						{
							if(data.errors.barcode)
							{
								error.text(error.text()  + " " +  data.errors.barcode.join(', '));
							}
						
							if(data.errors.barcode_type)
							{
								error.text(error.text()  + " " +  data.errors.barcode_type.join(', '));
							}
						
							if(data.errors.item_type)
							{
								error.text(error.text()  + " " +  data.errors.item_type.join(', '));
							}
						}
					}
				}).fail(function(data, textStatus, errorThrown)
				{
					$("#barcode_new_response").text(errorThrown);
				});
			}
			else
			{
				var error = $("#barcode_new_response");
				if(data.custom_errors)
				{
					console.log("here");
					error.text(error.text() + " " + data.custom_errors[0].message);
				}
				
				if(data.errors)
				{
					if(data.errors.picture)
					{
						error.text(error.text()  + " " +  data.errors.picture.join(', '));
					}
				}
				
				return;
			}
		},
		error: function(data, textStatus, errorThrown)
		{
			$("#barcode_new_response").text(errorThrown);			
			return;
		}
	});	
	
	 
}