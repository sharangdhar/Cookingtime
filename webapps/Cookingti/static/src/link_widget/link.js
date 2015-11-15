var RESULTS_TIME = 200;

$(document).ready(function()
{"use strict";

	
    $("#bulk_sidebar_add_panel").click(function()
    {
        $("#add_link").toggle(200);
    });
    
    $("#add_link_text").keypress(function(e)
    {
		link_search(e);
    });
    
    $("body").click(function()
    {
        $("#add_link_results").hide(RESULTS_TIME);
        $("#add_link_no_results").hide(RESULTS_TIME);
		
        check_overhang($("#add_link_results"));
		check_overhang($("#add_link_no_results"));
    });
    
    $(window).resize(check_overhang);
    
    
});

function link_search(e)
{"use strict";

	var input = $("#add_link_text");
	var type = input.attr("data-type") == "food" ? "recipe" : "food";
	var val = input.val();
	
	$.get("/search", {type: type, query: val, page:'item'}).done(function(data)
	{
		var results = $("#add_link_results");
		results.html(data);
		
		show_dropdown(results);
		check_overhang(results);

	}).fail(function(data)
	{
		check_overhang($("#add_link_no_results"));
	});

	
}

function check_overhang(div)
{"use strict";

    var page = $("#page");
    var overhang = div.offset().top + div.height() - (page.offset().top + page.height());
    
    
    if(div.css("display") === "none" || (overhang <= 0 && page.css("min-height") > 0))
    {
        page.css("min-height", "0px");
    }
    else
    {
        page.css("min-height", page.height() + overhang + 50);
    }
}

function show_dropdown(div)
{
	div.css("width", $("#bulk_sidebar_panel").width());
	div.show(RESULTS_TIME);
}

/*
var no_items = $("#no_linked_items");
if(no_items.length > 0)
{
no_items.remove();
}
*/