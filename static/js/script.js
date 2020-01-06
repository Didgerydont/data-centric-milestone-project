$(document).ready(function(){
    // nav
   $(".dropdown-trigger").dropdown();
    //Collapsible readrecipe.html
    $('.collapsible').collapsible();

    // search form on readrecipe
    $("#sendForm").click(function () {
        if ($('#sendForm').html() != '') {
            $("#search-form").submit();
        }
    });
});


    