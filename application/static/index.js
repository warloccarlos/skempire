    function deleteNote(noteId){
        fetch('/delnote',{
            method: 'POST',
            body: JSON.stringify({noteId:noteId})
        }).then((_res) => {
            window.location.href = '/';
        });
    }

    $(document).ready(function(){
        $("#sidebarCollapse").click(function(){
            $("#collapseNavBar").toggle('slow');
        });
    });

    $(document).ready(function(){
        $("#title").slideDown("slow");
    });

    $(document).ready(function(){
        $('#pen, #tester, #ap, #dso, #csp, #web, #dev').slideDown('slow');
    });

    $(document).ready(function(){
        $("#detBtn").click(function(){
            $('#details').slideToggle('slow')
        });
    });