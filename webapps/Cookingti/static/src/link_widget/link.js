var RESULTS_TIME = 200;

$(document).ready(function()
{"use strict";

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


	


    $("#bulk_sidebar_add_panel").click(function()
    {
        $("#add_link").toggle(200);
    });
    
    $("#add_link_text").keypress(function(e){link_search(e);});
	$(".bulk_sidebar_delete").click(function(e){link_delete(e);});
    
    $("body").click(function()
    {
        $("#add_link_results").hide(RESULTS_TIME);
        $("#add_link_no_results").hide(RESULTS_TIME);
		
        check_overhang($("#add_link_results"));
		check_overhang($("#add_link_no_results"));
    });
    
    $(window).resize(function(e){check_overhang($("#add_link_results"));});
    
    
});

function link_delete(e)
{"use strict";

	var target = $(e.target);

	var item_id = target.attr("data-item_id");
	var link_id = target.attr("data-link_item_id");
	var link_type = target.attr("data-link_item_type");
	
	$.post("/del_link", {item_id: item_id, link_id: link_id, link_type: link_type}).done(function(data)
	{
		target.closest('.bulk_sidebar_inner_panel').remove();
	}).fail(function(data)
	{
	});
	
}

function link_search(e)
{"use strict";

	var input = $("#add_link_text");
	var type = link_to_type();
	var val = input.val();
	
	$.get("/search", {type: type, query: val, page:'item'}).done(function(data)
	{
		$("#add_link_no_results").hide(RESULTS_TIME);
		
		var results = $("#add_link_results");
		results.html(data);
		
		var items = $(".bulk_sidebar_inner_panel");
		items.click(function(e){add_link(e);});

		
		show_dropdown(results);
		check_overhang(results);

	}).fail(function(data)
	{
		$("#add_link_results").hide(RESULTS_TIME);
		
		var section = $("#add_link_no_results");
		show_dropdown(section);
		check_overhang(section);
	});

	
}

function add_link(e)
{
	var item_id = $("#bulk_sidebar_panel").attr("data-id");
	var link_id = $(e.target).closest(".bulk_sidebar_inner_panel").attr("data-id");
	var link_type = link_to_type();
	
	$.post("/post_link", {item_id:item_id, link_id:link_id, link_type:link_type}).done(function(data)
	{
		var new_html = $(data);
		new_html.find('button').click(function(e){link_delete(e);});
		$("#bulk_sidebar_inner_wrapper").append(new_html);
		var linked = $("#no_linked_items");
		if(linked.length > 0)
		{
			linked.remove();
		}
		
	}).fail(function(data)
	{
		console.log("add fail");
		console.log(data.responseText);
	});
}

function link_to_type()
{
	return $("#add_link_text").attr("data-type") == "food" ? "recipe" : "food";
}
function check_overhang(section)
{"use strict";

    var page = $("#page");
    var overhang = section.offset().top + section.height() - (page.offset().top + page.height());
    
    
    if(section.css("display") === "none" || (overhang <= 0 && page.css("min-height") > 0))
    {
        page.css("min-height", "0px");
    }
    else
    {
        page.css("min-height", page.height() + overhang + 50);
    }
}

function show_dropdown(section)
{
	section.css("width", $("#bulk_sidebar_panel").width());
	section.show(RESULTS_TIME);
}

/*
var no_items = $("#no_linked_items");
if(no_items.length > 0)
{
no_items.remove();
}
*/