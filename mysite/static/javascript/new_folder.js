function NewFolder(){
    $.ajax({
        type:'GET',
        url: new_folder, 
        success: function(redirectResponse) {
            // $('body').html(redirectResponse);
            $("#section").load(new_folder);
        }
    });
}

$(document).on("submit", "#new_folder_form", function(event) {
    event.stopPropagation();
    event.preventDefault();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: new_folder,
        data: formData,
        success: function() {
            $("#section").load(" #wrapper2");
            $('#aside1').load(' #content-block');
        }
    })
});


