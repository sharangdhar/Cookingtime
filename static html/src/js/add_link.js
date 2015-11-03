$(document).ready(function()
{
    $("#bulk_sidebar_add_panel").click(function()
    {
        $("#add_link").toggle(200);
    });
    
    $("#add_link_text").keypress(function()
    {
        var results = $("#add_link_results");
        results.css("width", $("#bulk_sidebar_panel").width());
        $("#add_link_results").show(200);
        
        check_overhang();
        /*
        var page = $("#page");
        var overhang = results.offset().top + results.height() - (page.offset().top + page.height());
        if(overhang > 0)
        {
            page.css("min-height", page.height() + overhang + 50);
        }
        */

    });
    
    $("body").click(function()
    {
        $("#add_link_results").hide(200);
        check_overhang();
    });
    
    $(window).resize(check_overhang);
    
    
});


function check_overhang()
{
    var results = $("#add_link_results");
    var page = $("#page");
    var overhang = results.offset().top + results.height() - (page.offset().top + page.height());
    
    
    if(results.css("display") === "none" || (overhang <= 0 && page.css("min-height") > 0))
    {
        page.css("min-height", "0px");
    }
    else
    {
        page.css("min-height", page.height() + overhang + 50);
    }
}