$(document).ready(function()
{
	$('#enter_submit').click(function(e){submit_time(e);});
	
	
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
});

function submit_time(e)
{
	
	
    $("#enter_mass_error").remove();
    $(".enter_error").remove();
	
	
    var mass = $('#enter_mass').val();
    if(mass === "" || isNaN(mass))
    {
        $("#enter_mass_row").append($("<span id='enter_mass_error'>Enter valid value</span>"));
        return;
    }
    mass = parseFloat(mass);
    
    var mass_unit = $('#enter_unit option:selected').val();
    if(mass_unit === 'lb')
    {
        mass = lb_to_kg(mass);
    }
    if(mass_unit === 'oz')
    {
        mass = oz_to_kg(mass);
    }
    
	
	sec = get_sec();
	if(sec === 0)
	{
		$("#calc_input_row").append($("<span id='enter_input_error'>Enter valid value</span>"));
		return;
	}
	else
	{
		$('#enter_input_error').remove();
	}
	
	var watts = parseInt($('#calc_btn').attr('data-wattage'));
	var joules = watts * sec;
	
	var state =$('#enter_state option:selected').val();

	
	// Take care of extra energy for melting
	if(state === "frozen") 
	{
		var enth_fuse = 334; // J/g
		joules -= (enth_fuse * (mass*1000));
	}
	if(joules < 0)
	{
		return; // Shouldn't have been enough time to melt everything
	}
	
	// get dT (change in temperature)
	var start_state = $('#enter_state option:selected').val();
	var dT = get_dT(start_state);
	
	// Calculate specific heat
	var cp = joules / ((mass * 1000) * dT);

	
	var item_id = $('#enter_submit').attr('data-id');

	$.post('/post_time', {item_id:item_id, constant:cp}).done(function(data)
	{
		if(data.status == 'success')
		{
			$('#calc_btn').attr("data-constant", data.result);
			$("#calc_input_row").append($("<span id='enter_input_error'>Success!</span>"));
		}
		else
		{
			var error;
			if(data.custom_errors)
			{
				error = data.custom_errors[0].message;			
			}
			else if(data.errors)
			{
				if(data.errors.hasOwnProperty('item_id'))
				{
					error = data.errors.item_id[0];
				}
				else if(data.errors.hasOwnProperty('constant'))
				{
					error = "Error";
				}
			}
			
			$("#calc_input_row").append($("<span class='enter_input_error'>" + error + "</span>"));	
		}
		
	}).fail(function()
	{
		$("#calc_input_row").append($("<span id='enter_input_error'>Error</span>"));	
	});
	
}




function get_sec()
{
	var min = $('#enter_min').val();
	var sec = $('#enter_sec').val();
	
	if(min === '')
	{
		min = 0;
	}
	else
	{
		min = parseInt(min);
		if(isNaN(min))
		{
			min = 0;
		}
	}
	
	
	if(sec === '')
	{
		sec = 0;
	}
	else
	{
		sec = parseInt(sec);
		if(isNaN(sec))
		{
			sec = 0;
		}
	}
	
	return sec + (60 * min);
}