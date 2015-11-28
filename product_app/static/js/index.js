$(document).ready(function(){
    setTimeout(function(){
        $('.grid').masonry({
            // options
            itemSelector: '.grid-item',
        });
    }, 300);
        
        
    
    //Show Grid View
    $("#gridBtn").click(function(){
	if ($("#listView").is(':visible')) {
	    $("#listView").fadeOut(300,function(){
		$("#gridView").fadeIn(300);
	    });
	}
    });
    
    //Show List View
    $("#listBtn").click(function(){
	if ($("#gridView").is(':visible')) {
	    $("#gridView").fadeOut(300,function(){
		$("#listView").fadeIn(300);
	    });
	}
    });
    
        
});