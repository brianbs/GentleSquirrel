window.onload = function(){
    console.log("Hello, world!");
    $("#submitsong").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        song_title = $("#songsearch").val();
        if(song_title.length <= 0){
            $("#lengthwarning").show();
        }
        else{
            var search = {
                source : song_title
            };
            $( "#submitsong" ).hide();
            $( "#ajaxgif" ).show();
            $.ajax({
                url: '/gsplus/api/v0.1/queue',
                type: 'POST',
                contentType: "application/json",
                dataType: 'json',
                data: JSON.stringify(search),
                success: function( data ) {
                    $( "#submitsong" ).show();
                    $( "#ajaxgif" ).hide();
                    $("#postnotification").html( data.message );
                    $("#postnotification").show();
                }
            });
        }
    });
    $("#clearbutton").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        var request = {
            playlist : []
        }
        $.ajax({
            url: '/gsplus/api/v0.1/queue',
            type: 'PUT',
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify(request),
            success: function( data ) {
                $("#queuenotification").html( "Playlist cleared" );
                $("#queuenotification").show();
            }
        });
    } );
    $("#nextbutton").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        var request = {
            operation : "next"
        }
        $.ajax({
            url: '/gsplus/api/v0.1/queue/currentsong',
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify(request),
            success: function( data ) {
                $("#queuenotification").html( "Song skipped" );
                $("#queuenotification").show();
            }
        });
    });
    $("#playbutton").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        var request = {
            playback : "play"
        }
        $.ajax({
            url: '/gsplus/api/v0.1/state/playback',
            type: 'PUT',
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify(request),
            success: function( data ) {
                $('#statenotification').html( "Resumed" );
                $('#statenotification').show();
            }
        });
    } );
    $("#pausebutton").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        var request = {
            playback : "pause"
        }
        $.ajax({
            url: '/gsplus/api/v0.1/state/playback',
            type: 'PUT',
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify(request),
            success: function( data ) {
                $('#statenotification').html( "Paused" );
                $('#statenotification').show();
            }
        });
    } );
    $("#volumeup").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        $.ajax({
            url: '/gsplus/api/v0.1/state/volume',
            type: 'GET',
            contentType: "application/json",
            dataType: 'json',
            success: function( data ) {
                var curr_vol = parseInt( data.volume );
                new_vol = curr_vol + 5;
                if(new_vol > 100){
                    new_vol = 100
                }
                request = {
                    volume: new_vol.toString()
                }
                $.ajax({
                    url: '/gsplus/api/v0.1/state/volume',
                    type: 'PUT',
                    contentType: "application/json",
                    dataType: 'json',
                    data: JSON.stringify( request ),
                    success: function( data ) {
                        $( "#volumenotification" ).show();
                        $( "#volumenotification" ).html( "Volume: " + data.volume );
                    }
                });
            }
        });
    } );
    $("#volumedown").click( function(){
        $('#lengthwarning').hide();
        $('#postnotification').hide();
        $('#queuenotification').hide();
        $('#statenotification').hide();
        $('#volumenotification').hide();
        $.ajax({
            url: '/gsplus/api/v0.1/state/volume',
            type: 'GET',
            contentType: "application/json",
            dataType: 'json',
            success: function( data ) {
                var curr_vol = parseInt( data.volume );
                new_vol = curr_vol - 5;
                if(new_vol < 0){
                    new_vol = 0
                }
                request = {
                    volume: new_vol.toString()
                }
                $.ajax({
                    url: '/gsplus/api/v0.1/state/volume',
                    type: 'PUT',
                    contentType: "application/json",
                    dataType: 'json',
                    data: JSON.stringify( request ),
                    success: function( data ) {
                        $( "#volumenotification" ).show();
                        $( "#volumenotification" ).html( "Volume: " + data.volume );
                    }
                });
            }
        });
    } );
}
