$(document).ready(function()
{
	$('#recipe_edit_button').click(function(e){recipe_edit(e);});
	$('#recipe_submit_button').click(function(e){recipe_submit(e);});
	
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

function recipe_edit(e)
{
	$('#recipe_content').toggle(200);
	$('#recipe_form').toggle(200);
}

function recipe_submit(e)
{
	var text = $("#recipe_text").val();
	var item_id = $('#recipe_submit_button').attr('data-id');
	
	$.post('/post_recipe', {item_id:item_id, text:text}).done(function(data)
	{
		if(data.status == 'success')
		{
			$('#recipe_content').html(data.html);
			recipe_edit();
		}
		else
		{
			gen_errors = '';
			if(data.custom_errors)
			{
				for(i = 0; i < data.custom_errors.length; i++)
				{
					sep = ', ';
					if(i === 0){sep = '';}
					gen_errors = gen_errors + sep + data.custom_errors[i].message;
				}
			}
			
			if(data.errors)
			{
				text_errors = '';
				if(data.errors.text)
				{
					for(i = 0; i < data.errors.text.length; i++)
					{
						sep = ', ';
						if(i === 0){sep = '';}
						text_errors = text_errors + sep + data.errors.text[i];
					}
				}
				
				if(data.errors.item_id)
				{
					for(i = 0; i < data.errors.item_id.length; i++)
					{
						sep = ', ';
						if(gen_errors === ''){sep = '';}
						gen_errors = gen_errors + sep + data.errors.item_id[i];
					}
				}
				
				$("#recipe_text_error").text(text_errors);
			}
			
			$("#recipe_error").text(gen_errors);
		}
		
		
	}).fail(function(data)
	{
		$("#recipe_error").text("Error");
	});
}