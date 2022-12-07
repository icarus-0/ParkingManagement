$(document).ready(function(){ 
    $("#zone_a_btn_div").hide();
    $("#zone_b_btn_div").hide();
    $("#zone_c_btn_div").hide();

    $('#zone_a_btn').click(function(){
        
        $("#zone_a_btn_div").show();
        $("#zone_b_btn_div").hide();
        $("#zone_c_btn_div").hide();
    });

    $('#zone_b_btn').click(function(){
        
        $("#zone_a_btn_div").hide();
        $("#zone_b_btn_div").show();
        $("#zone_c_btn_div").hide();
    });

    $('#zone_c_btn').click(function(){
        
        $("#zone_a_btn_div").hide();
        $("#zone_b_btn_div").hide();
        $("#zone_c_btn_div").show();
    });
});


$(document).ready(function(){ 
    
});
