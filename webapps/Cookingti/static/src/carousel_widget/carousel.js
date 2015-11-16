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
	
	
	
	
	
    $("#carousel_left_button").click(function(){slide("left");});
    $("#carousel_right_button").click(function(){slide("right");});
	$("#carousel_submit").click(function(e){upload(e); return false;});
    $("#carousel_upload_button").click(function()
    {
        $("#carousel_upload_box").toggle(200);
        
        var btn = $("#carousel_upload_button");
        if(btn.text() === "Upload")
        {
            btn.text("Cancel");
        }
        else
        {
            btn.text("Upload");
        }
    });
    
	
	
});

function upload(e)
{
	console.log("in upload");
	
	var fd = new FormData();
	
	console.log($("#carousel_id").val());
	console.log($("#carousel_type").val());
	
	fd.append('page_type', $("#carousel_type").val());
	fd.append('item_id', $("#carousel_id").val());
	fd.append('picture', $("#carousel_file")[0].files[0]);
	
	
	$.ajax(
	{
        url: '/post_img',
        data: fd,
        processData: false,
		contentType: false,
        type: 'POST',
        success: function (data) 
		{
			console.log("success");
            console.log(data);
        },
		error: function(data)
		{
			console.log("error");
			console.log(data);
		}
    });
	
	return false;
}

function slide(direction)
{
    var slider = $("#carousel_slider");
    var left = parseInt(slider.css("left"));
    
    // If we're already at the end, don't go any further
    /*
    if( (left >= 0 && direction === "left") || (left <= (-1 * slider.width()) && direction === "right") )
    {
        return;
    }
    */
    
    var offset = 0.5 * slider.width();
    if(direction === "right")
    {
        offset = -1 * offset;
    }
    
    
    // If it would go too far, only go as far as the end
    if(direction === "left" && offset + left >= 0)
    {
        offset = (-1 * left) + 30;
    }
    if(direction === "right" && offset + left <= (-1 * slider.width()) + $("#photo_panel").width() - 30)
    {
        offset = (-1 * left) - slider.width() + $("#photo_panel").width() - 30;
    }

    
    
    var new_left = left + offset;
    var new_left_str = new_left.toString() + "px";
    
    slider.animate({"left":new_left_str}, 300);
}