function ShowFile(file_id){
    $.ajax({
        type:'GET',
        url: show_file,
        data: {csrfmiddlewaretoken: csrfToken, "file_id": file_id},
        success: function() {
            $('#section').load(' #wrapper2')
            $('#aside2').load(' #aside2')

            // var code = $("#wrapper2");
            // var editor = CodeMirror.fromTextArea(code, {
            //     linenumbers : true
            // });
        }
    })
}