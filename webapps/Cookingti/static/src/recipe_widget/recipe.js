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
		$('#recipe_content').html(data);
		recipe_edit();
		
	}).fail(function(data)
	{
		console.log('recipe submit fail');
	});
}