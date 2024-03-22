function NewFile(){
    $.ajax({
        type:'GET',
        url: new_file,
        success: function(redirectResponse) {
            // $('body').html(redirectResponse);
            $("#section").load(new_file);
        }
    });
}

$(document).on("submit", "#new_file_form", function(event) {
    event.stopPropagation();
    event.preventDefault();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: new_file,
        data: formData,
        success: function(redirectResponse) {
            // $('body').html(redirectResponse);
            $("#section").load( fix_sections);
            // $('#aside1').load(' #content-block');
        }
    })
});
