$(document).ready(function()
{
    var stars = $(".stars_widget");
    for(var i = 0; i < stars.length; i++)
    {
        build_stars(stars.eq(i));
    }
    
    stars.children().mouseover(function(e){stars_mouseover(e);});
    stars.children().mouseleave(function(e){stars_mouseleave(e);});
    stars.children().mouseup(function(e){stars_up(e);});
});


function build_stars(widget)
{
    for(i = 1; i <= 5; i++)
    {
        widget.append($('<span data-num="' + i + '">&#9733;</span>'));
    }
    
    set_stars(widget, parseInt(widget.attr('data-stars')));
}

function stars_mouseover(e)
{
    var max = parseInt($(e.target).attr('data-num'));

    var widget = $(e.target).parent();
    set_stars(widget, max);
    
}

function stars_mouseleave(e)
{
    var widget = $(e.target).parent();
    set_stars(widget, parseInt(widget.attr('data-stars')));
}

function stars_up(e)
{
    var val = parseInt($(e.target).attr('data-num'));
    var widget = $(e.target).parent();
    widget.attr("data-stars", val);
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