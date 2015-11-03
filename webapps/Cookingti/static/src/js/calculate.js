$(document).ready(function()
{
    $('#calc_btn').click(calculate);
    $('#calc_mass').keypress(function(e)
    {
        if(e.which == 13)
        {
            calculate();
        }
    });
});


function calculate()
{
    var mass = parseFloat($('#calc_mass').val());
    var mass_unit = $('#calc_unit option:selected').val();
    if(mass_unit === 'lb')
    {
        mass = lb_to_kg(mass);
    }
    if(mass_unit === 'oz')
    {
        mass = oz_to_kg(mass);
    }
    
    // else its already in kg
    
    var btn = $('#calc_btn');
    var constant = parseFloat(btn.attr('data-constant'));
    var wattage = parseFloat(btn.attr('data-wattage'));
    
    var end_temp = 373.15; // boiling in K
    var state = $('#calc_state option:selected').val();
    var start_temp = 0;
    if(state === 'frozen')
    {
        start_temp = 255.15; // recomended freezer temp in K
    }
    else if (state === 'refrigerated')
    {
        start_temp = 274.75; // recomended refrigerator temp in K
    }
    else if (state === 'room')
    {
        start_temp = 294.15;
    }
    var dt = end_temp - start_temp;
    
    var sec = (constant * (mass * 1000) * dt) / wattage;


    // Add time if frozen
    if(state == 'frozen')
    {
        var enth_fuse = 334; // J/g
        var extra = (enth_fuse * (mass * 1000)) / wattage; 
        sec += extra;
    }
    

    min = sec / 60;

    var left_over = min - Math.floor(min);
    if(left_over > 0.017)
    {
        var extra_sec = left_over * 60;
        $('#calc_ret').val(Math.floor(min) + ' min, ' + Math.floor(extra_sec) + ' sec');
    }
    else
    {
        $('#calc_ret').val(min + ' min');
    }
    
    return;
}


function lb_to_kg(lb)
{
    return lb * 0.453592;
}

function oz_to_kg(oz)
{
    return oz * 0.0283495;
}