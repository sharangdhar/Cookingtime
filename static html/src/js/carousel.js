$(document).ready(function()
{
    $("#carousel_left_button").click(function(){slide("left");});
    $("#carousel_right_button").click(function(){slide("right");});
    
});

function slide(direction)
{
    slider = $("#carousel_slider");
    left = parseInt(slider.css("left"));
    
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

    
    
    new_left = left + offset;
    new_left_str = new_left.toString() + "px";
    
    slider.animate({"left":new_left_str}, 300);
}