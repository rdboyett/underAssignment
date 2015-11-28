$(document).ready(function(){
    
    $("#id_quantity").on("change", function(){
        var quantity = $(this).val();
        var price = $("#id_price").val();
        $("#currentPrice").html(parseFloat(price*quantity).toFixed(2));
        $("#quantityTickets").html(" "+quantity);
        if (quantity>1) {
            $("#plural").html('s');
        }else{
            
            $("#plural").html('');
        }
    });
    
    //Limit the maximum value of quantity.
    $("form").validate({
        rules: {
            quantity: {
              required: true,
              max: maxQuantity
            }
        }
    });
    $("#id_phone").mask("(999) 999-9999");
    
    
    $('form').ajaxForm({
        success:       function(responseText){
            if (responseText.error) {
                alert(responseText.error);
            }else{
	       alert("An email has been sent for resetting your password.")
               $("#myModal").modal('hide');
            }
        },
        dataType:  'json',
        timeout:   4000 
    }); 
});