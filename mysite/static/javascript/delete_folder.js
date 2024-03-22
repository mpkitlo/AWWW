function DeleteFolder(folder_id){
    $.ajax({
        type:'GET',
        url: delete_folder,
        data: {csrfmiddlewaretoken: csrfToken, "folder_id": folder_id},
        success: function() {
            $('#aside1').load(' #content-block')
        }
    });
}