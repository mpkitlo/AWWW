function FixSections(){
    $.ajax({
        type:'GET',
        url: fix_sections,
        success: function(redirectResponse) {
            // $('body').html(redirectResponse);
            $("#section").load(fix_sections);
        }
    });
}

$(document).on("submit", "#edit_sections", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: fix_sections,
        data: formData , 
    }).done(function (response) {
        if (response.redirect) {
            $.ajax({
                type: 'GET',
                url: response.redirect,
                data: csrfToken,
                success: function(redirectResponse) {
                    $("#section").load(" #wrapper2");
                    $('#aside1').load(' #content-block');
                },
            });   
        }
    });
});