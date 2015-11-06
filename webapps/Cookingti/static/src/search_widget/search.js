$(document).ready(function()
{
	$('#search_button').click(search);
});

function search()
{
	$(document).prop('title', 'Cookingti.me | Search');
	$('#hs_title').text("Search Results");
	
	
	var sections = 
	[
		{id:'foods_col', type:'food', html:''},
		{id:'recipies_col', type:'recipe', html:''},
		{id:'equipment_col', type:'equip', html:''}
	];
	
	for(i = 0; i < sections.length; i++)
	{
		var sect = sections[i];
		var val = $('#search_input').val();
		
		$.get('/search', {type: sect.type, query: val}).done(search_ret);
	}
}

function search_ret(data)
{
	if(data.status == "Success")
	{
		console.log("Success");
		console.log(data);
	}
}