function DownloadFile(){
    var xhr = $.ajax({
        type:'GET',
        url: download_file,
        xhrFields: {
            responseType: 'blob'
        },
        success: function(response) {
            try {
                var link = document.createElement('a')
                link.href = window.URL.createObjectURL(response)
                link.download = xhr.getResponseHeader('Content-Disposition') + '.asm';
                link.click()
                URL.revokeObjectURL(link.href)
            }  catch (error) {
                alert("Nie ma co pobrac. Kod sie nie kompiluje/nie został skompilowany")
            }
        }
    });
}