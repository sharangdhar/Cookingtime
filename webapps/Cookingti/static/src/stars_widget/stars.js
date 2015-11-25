$(document).ready(function()
{
    var stars = $(".stars_widget");
    for(var i = 0; i < stars.length; i++)
    {
        build_stars(stars.eq(i));
    }
    
	/*
    stars.children().mouseover(function(e){stars_mouseover(e);});
    stars.children().mouseleave(function(e){stars_mouseleave(e);});
    stars.children().mouseup(function(e){stars_up(e);});
	*/
});


function build_stars(widget)
{
    for(i = 1; i <= 5; i++)
    {
        widget.append($('<span data-num="' + i + '">&#9733;</span>'));
    }
	
    widget.children().mouseover(function(e){stars_mouseover(e);});
    widget.children().mouseleave(function(e){stars_mouseleave(e);});
    widget.children().mouseup(function(e){stars_up(e);});
	
	
    var hidden = widget.parent().children(".stars");
    set_stars(widget, parseInt(hidden.val()));
}

function stars_mouseover(e)
{
	var target = $(e.target);
    var widget = target.parent();

    var max = parseInt(target.attr("data-num"));
		
    set_stars(widget, max);
    
}

function stars_mouseleave(e)
{
    var widget = $(e.target).parent();
	var hidden = widget.parent().children(".stars");
	
    set_stars(widget, parseInt(hidden.val()));
}

function stars_up(e)
{
	var target = $(e.target);
    var widget = target.parent();
	var hidden = widget.parent().children(".stars");
	
    var val = parseInt(target.attr("data-num"));
	hidden.val(val);
	
	set_stars(widget, val);
}

function set_stars(widget, num)
{
    var stars = widget.children();
    
    for(var i = 0; i < 5; i++)
    {
        if(i < num)
        {
            stars.eq(i).html("&#9733;");
        }
        else
        {
            stars.eq(i).html("&#9734;");
        }
    }
}