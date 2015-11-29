$(document).ready(function(){
    
    $("#id_quantity").on("change", function(){
        var quantity = $(this).val();
        var price = $("#id_price").val();
        $(".currentPrice").html(parseFloat(price*quantity).toFixed(2));
        $(".quantityTickets").html(" "+quantity);
        if (quantity>1) {
            $(".plural").html('s');
        }else{
            
            $(".plural").html('');
        }
    });
    
    //Limit the maximum value of quantity.
    $("#purchase-form").validate({
        rules: {
            quantity: {
              required: true,
              max: maxQuantity
            }
        }
    });
    $("#id_phone").mask("(999) 999-9999");
    
    //Pick up the submit button and check for errors then display the confirmation modal before submitting the form
    $("#submitCheckBtn").click(function(){
        if ($('#purchase-form').valid()){
            $("#orderConfirm-modal").modal('show');
        }
    });
    
    
    $('#purchase-form').ajaxForm({
        beforeSubmit:  function(){
            $("#shade").fadeIn(300);
            $("#spinnerHolder").fadeIn(300);
        },
        success:       function(responseText){
            if (responseText.error) {
                alert(responseText.error);
            }else if (responseText.success){
                var purchaseID = responseText.success.purchaseID;
                window.location.href = "/success/"+purchaseID;
            }else{
                var errorMessage = "Sorry, some errors were found:\n";
                for (var field in responseText) {
                    errorMessage = errorMessage.concat(field+": ")
                    errorMessage = errorMessage.concat(responseText[field][0].message+"\n");
                }
                alert(errorMessage);
            }
        },
        dataType:  'json',
        timeout:   4000 
    }); 
});