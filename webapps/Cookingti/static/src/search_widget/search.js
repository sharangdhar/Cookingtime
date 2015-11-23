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
		$('#search_foods_wrapper').html(data);
		
		$('#home_pre').hide(200);
		$('#search_results').show(200);
		$(document).prop('title', 'Cookingti.me | Search');
		
	}).fail(function(data)
	{
		$('#search_foods_wrapper').html("<h3>No results</h3>");
		
	});




	$.get('/search', {type: "recipe", query: val, page:'search'}).done(function(data)
	{	
		$('#search_recipe_wrapper').html(data);
		$('#home_pre').hide(200);
		$('#search_results').show(200);
		$(document).prop('title', 'Cookingti.me | Search');

	}).fail(function(data)
	{
		$('#search_recipe_wrapper').html("<h3>No results</h3>");
		
	});
	
	
	
	
	$.get('/search', {type: "equipment", query: val, page:'search'}).done(function(data)
	{	
		$('#search_equipment_wrapper').html(data);
		$('#home_pre').hide(200);
		$('#search_results').show(200);
		$(document).prop('title', 'Cookingti.me | Search');

	}).fail(function(data)
	{
		$('#search_equipment_wrapper').html("<h3>No results</h3>");
		
		
	});
}
