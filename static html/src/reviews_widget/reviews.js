$(document).ready(function()
{
    $("#review_sort").change(function(e){review_sort(e);}); 
});

function review_sort(e)
{
    var order = $( "#review_sort option:selected" ).attr("value");
    var reviews = $(".review");
    

    switch(order)
    {
    case "highest":
        reviews.sort(review_sort_highest);
        break;
    case "lowest":
        reviews.sort(review_sort_lowest);
        break;
    case "newest":
        reviews.sort(review_sort_newest);
        break;
    case "oldest":
        reviews.sort(review_sort_oldest);
        break;
    }
    
    
    reviews.detach().appendTo($("#reviews_wrapper"));
    
}

function review_sort_newest(a, b)
{    
    var a_sort = review_get_date(a);
    var b_sort = review_get_date(b);
    
    
    if(a_sort < b_sort)
    {
        return 1;
    }
    else if(a_sort > b_sort)
    {
        return -1;
    }
    
    return 0;
}

function review_sort_oldest(a, b)
{    
    var a_sort = review_get_date(a);
    var b_sort = review_get_date(b);
    
    
    if(a_sort > b_sort)
    {
        return 1;
    }
    else if(a_sort < b_sort)
    {
        return -1;
    }
    
    return 0;
}


function review_sort_highest(a, b)
{    
    var a_sort = review_get_stars(a);
    var b_sort = review_get_stars(b);
    
    if(a_sort < b_sort)
    {
        return 1;
    }
    else if(a_sort > b_sort)
    {
        return -1;
    }
    
    return 0;
}

function review_sort_lowest(a, b)
{    
    var a_sort = review_get_stars(a);
    var b_sort = review_get_stars(b);
    
    if(a_sort > b_sort)
    {
        return 1;
    }
    else if(a_sort < b_sort)
    {
        return -1;
    }
    
    return 0;
}

function review_get_stars(review)
{
    return parseInt($(review).children(".review_top_matter").children(".review_rating").attr("data-stars"));
}

function review_get_date(review)
{
    return Date.parse($(review).children(".review_top_matter").children(".review_date").text());
}