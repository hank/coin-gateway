function forAllRPCs(func) {
    $('#info tr[class="rpc"]').remove();
    $.getJSON( "/api", function( data ) {
        for(i=0; i<data.length; ++i) {
            func(data[i]);
        }
    })
        .fail(function() {
            console.log("Failed to fetch");
        });
}

