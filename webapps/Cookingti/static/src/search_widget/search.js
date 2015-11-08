$(document).ready(function()
{
	$('#search_button').click(search);
	$(document).keypress(function(e)
	{
		if(e.which == 13)
		{
			search();
		}
	});
});

function search()
{	
	var sections = 
	[
		{id:'foods_col', type:'food'},
		{id:'recipies_col', type:'recipe'},
		{id:'equipment_col', type:'equipment'}
	];
	

	var val = $('#search_input').val();
		
	$.get('/search', {type: "food", query: val, page:'search'}).done(function(data)
	{
		$(document).prop('title', 'Cookingti.me | Search');
		$('#hs_title').text("Search Results");
	
		$('#foods_wrapper').html(data);
	}).fail(function(data)
	{
		$('#foods_wrapper').html("<h3>No results</h3>");
		
	});


	$.get('/search', {type: "recipes", query: val, page:'search'}).done(function(data)
	{
		$(document).prop('title', 'Cookingti.me | Search');
		$('#hs_title').text("Search Results");
	
		$('#recpies_wrapper').html(data);
	}).fail(function(data)
	{
		$('#recpies_wrapper').html("<h3>No results</h3>");
		
	});
	
	
	$.get('/search', {type: "equipment", query: val, page:'search'}).done(function(data)
	{
		$(document).prop('title', 'Cookingti.me | Search');
		$('#hs_title').text("Search Results");
	
		$('#equipment_wrapper').html(data);
	}).fail(function(data)
	{
		$('#equipment_wrapper').html("<h3>No results</h3>");
		
	});
}
