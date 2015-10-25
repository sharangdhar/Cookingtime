$(document).ready(function()
{
    $("#carousel_left_button").click(function(){slide("left");});
    $("#carousel_right_button").click(function(){slide("right");});
    
});

function slide(direction)
{
    slider = $("#carousel_slider");
    
    left = parseInt(slider.css("left"));
    
    if( (left > 0 && direction === "left") || (left < (-1 * slider.width()) && direction === "right") )
    {
        return;
    }
    
    var offset = slider.width() - 200;
    if(direction === "right")
    {
        offset = -1 * offset;
    }
    
    new_left = left + offset;
    new_left_str = new_left.toString() + "px";
    
    slider.animate({left:new_left_str}, 300);
}