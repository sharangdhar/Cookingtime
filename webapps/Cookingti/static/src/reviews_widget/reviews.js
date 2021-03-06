$(document).ready(function()
{
	$(".review_submit").click(function(e){submit_review(e);});
	$(".review_edit").click(function(e){review_edit(e);});
	
	
    $("#review_sort").change(function(e){review_sort(e);}); 
    
    $('#review_add_panel').click(function()
    {
        $('#new_review').toggle(200);
    });
	
});

function review_edit(e)
{
	var review = $(e.target).closest(".review");
	review.children(".review_display").toggle(200);
	review.children(".review_form").toggle(200);
}

function submit_review(e)
{"use strict";

	var par = $(e.target).closest(".review_form");
		
	var title = par.children(".edit_review_title").eq(0).val();
	var title_error = par.children(".review_title_error").eq(0);
	title_error.text("");
	
	var stars = par.children(".stars").eq(0).val();
	var stars_error = par.children(".stars_error").eq(0);
	stars_error.text("");
	
	var text = par.children(".edit_review_text").eq(0).val();
	var text_error = par.children(".text_error").eq(0);
	text_error.text("");
	
	var page_type = par.children(".page_type").eq(0).val();
	var item_id = par.children(".item_id").eq(0).val();
	var review_id = par.children(".review_id").eq(0).val();
	var new_review = (review_id == "new");
	
	var general_error = par.children(".general_error").eq(0);
	
	$.post("/post_review", {title: title, stars:stars, review: text, page_type: page_type, item_id: item_id, review_id: review_id}).done(function(data)
	{
		
		if(data.status == "success")
		{
			title_error.text("");
			stars_error.text("");
			text_error.text("");
			
			general_error.text("Success!");
			var new_html = $(data.html);
			
			if(new_review)
			{
				$(e.target).closest("#reviews_panel").find("#reviews_wrapper").eq(0).prepend(new_html);
				$('#new_review').hide(200);
			}
			else
			{
				par.hide(200);
				par.closest(".review").replaceWith(new_html);
			}
			
			build_stars(new_html.find(".stars_widget"));
			
			$(".review_submit").unbind('click').click(function(e){submit_review(e);});
			$(".review_edit").unbind('click').click(function(e){review_edit(e);});
		}
		else
		{
			if(data.custom_errors)
			{
				general_error.text(data.custom_errors[0].message);
			}
			
			if(data.errors)
			{
				if(data.errors.title)
				{
					console.log(data.errors.title);
					console.log(data.errors.title.join(', '));
					var error1 = data.errors.title.join(', ');
					title_error.text(error1);
				}
				
				if(data.errors.stars)
				{
					var error2 = data.errors.stars.join(', ');
					stars_error.text(error2);
				}
				
				if(data.errors.review)
				{
					var error3 = data.errors.review.join(', ');
					text_error.text(error3);
				}
			}
		}
	}).fail(function(data)
	{
		general_error.text("Error!");
	});
	
	return false;
	
}

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
	console.log($(review));
    return parseInt($(review).find(".review_rating").attr("data-stars"));
}

function review_get_date(review)
{
    return Date.parse($(review).find(".review_date").text());
}