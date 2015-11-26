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
	
	
	
	
	$("#profile_edit_button").click(function(e)
	{
		$("#profile_table").toggle(100);
		$("#profile_form").toggle(200);
	});
	
	$("#profile_form_submit").click(profile_submit);
});

function profile_submit(e)
{"use strict";

	$("#profile_first_name_error").text("");
	$("#profile_last_name_error").text("");
	$("#profile_email_error").text("");
	$("#user.person.all.0.wattage").text("");
	

	var args = {};
	
	args.user_id = $("#profile_form_submit").attr("data-user_id");
	args.firstname = $("#profile_form_firstname").val();
	args.lastname = $("#profile_form_lastname").val();
	args.email = $("#profile_form_email").val();
	args.wattage = $("#profile_form_wattage").val();
	
	$.post('/edit_profile', args).done(function(data)
	{
		if(data.status == "success")
		{
			$("#table_first").text(data.data.firstname);
			$("#table_last").text(data.data.lastname);
			$("#table_email").text(data.data.email);
			$("#table_wattage").text(data.data.wattage);
			
			$("#profile_table").toggle(100);
			$("#profile_form").toggle(200);
		}
		else
		{
			
			if(data.custom_errors)
			{
				$("#profile_form_general_error").text(data.custom_errors.join(", "));
			}
			else
			{
				$("#profile_form_general_error").text("Error");			
			}
			
			
			if(data.errors)
			{
				if(data.errors.firstname)
				{
					console.log(data.errors.firstname.join(", "));
					$("#profile_first_name_error").text(data.errors.firstname.join(", "));
				}
				
				if(data.errors.lastname)
				{
					$("#profile_last_name_error").text(data.errors.lastname.join(", "));
				}
				
				if(data.errors.lastname)
				{
					$("#profile_email_error").text(data.errors.email.join(", "));
				}
				
				if(data.errors.lastname)
				{
					$("#profile_wattage_error").text(data.errors.wattage.join(", "));
				}
			}
			
			
		}

	}).fail(function(data)
	{
		$("#profile_form_general_error").text("Error");
	});
}