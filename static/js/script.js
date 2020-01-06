$(document).ready(function(){
   $(".dropdown-trigger").dropdown();

    // search form on readrecipe
    $("#sendForm").click(function () {
        if ($('#sendForm').html() != '') {
            $("#search-form").submit();
        }
    });
});


    