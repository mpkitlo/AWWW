function DeleteFile(file_id){
    $.ajax({
        type:'GET',
        url: delete_file,
        data: {"file_id": file_id},
        success: function() {
            $('#aside1').load(' #content-block')
            $('#section').load(' #wrapper2')
            $('#aside2').load(' #wrapper')
        }
    });
}