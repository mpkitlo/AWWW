$(document).on("submit", "#set_standard", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: standard,
        data: formData, 
        success: function() {
            $('#footer2').load(" #footer2");
        }
    });    
});

$(document).on("submit", "#set_optimizations", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: optimization,
        data: formData, 
        success: function() {
            $('#footer2').load(" #footer2");
        }
    });    
});

$(document).on("submit", "#set_procesor", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: procesor,
        data: formData, 
        success: function() {
            $('#footer2').load(" #footer2");
        }
    });    
});

$(document).on("submit", "#set_dependent", function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formData = $(this).serialize() + ('&csrfmiddlewaretoken=' + encodeURIComponent(csrfToken));
    $.ajax({
        type: "POST",
        url: dependent,
        data: formData, 
        success: function() {
            $('#footer2').load(" #footer2");
        }
    });    
});

