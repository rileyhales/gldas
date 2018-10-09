// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

thredds_wms_url = "http://127.0.0.1:7000/thredds/wms/testAll/";



// JQuery and AJAX Listeners/Controllers to let the user manipulate the map
$(document).ready(function() {


//////////////////////// LEAFLET CONTROLS ///////////////////////////////////////////////


//    Show the first layer from the list on load
    variable = $('#layers').val();
    color= $('#colors').val();
    newLayer(variable, color);
    getLegend(variable, color);
    newControls();

//    Listener for the variable picker menu (selectinput gizmo)
    $("#layers").change(function () {
        updateMap();
        });

//    Listener for the color changer
    $("#colors").change(function () {
        updateMap();
        });

//    Listener for the opacity select slider (rangeslider gizmo)
    $("#opacity").change(function () {
        timedLayer.setOpacity($('#opacity').val());
        });

//    Listener for the remove layers button (html button)
    $("#removal").click(function () {
        removeData()
        });


//////////////////////// HIGHCHARTS CONTROLS ///////////////////////////////////////////////

//  Generate a plot whenever the user draws a new point
    map.on("draw:created", function() {

        coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
        variable = $('#layers').val();
        data = {
            coords: coords,     // array or list in the format [[lat, lon], [lat, lon] ... etc
            variable: variable, // which of the variables available to get timeseries data for
            };

        console.log(data)

    // Ajax script to send the data for processing
        $.ajax({
            url:'/apps/gldas/generatePlot/',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function(result) {
                console.log(result);
                newHighchart(result);
                },
            });
        });

});