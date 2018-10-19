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

//  Sets the correct urls based on the time period
function setLinks(time, variable) {
    thredds_base = 'http://127.0.0.1:7000/thredds/';
    thredds_wms = thredds_base + 'wms/testAll/';
    thredds_wms += time + '.ncml';

//  If you choose to show all data
    if (time == 'all') {
        thredds_wms += 'alltimes.ncml';
    }
//  This should take care of selecting single year intervals
    return thredds_wms, time
}


// JQuery and AJAX Listeners/Controllers to let the user manipulate the map
$(document).ready(function() {

//  Load initial map data as soon as the page is ready
    variable = $('#layers').val();
    time = $("#times").val();
    color = $('#colors').val();
    setLinks(time, variable);
    newLayer(variable, color);
    newControls();
    legend.addTo(map);

//////////////////////// GENERAL CONTROLS ///////////////////////////////////////////////

    $("#times").change(function() {
        time = $("#times").val();
        variable = $('#layers').val();
        setLinks(time, variable);
        updateMap();
    });

//////////////////////// LEAFLET CONTROLS ///////////////////////////////////////////////

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

//////////////////////// HIGHCHARTS CONTROLS ///////////////////////////////////////////////

//  Generate a plot whenever the user draws a new point
    map.on("draw:created", function() {
        chart.hideNoData();
        chart.showLoading();

        coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
        variable = $('#layers').val();
        time = $("#times").val();
        data = {
            coords: coords,         // array or list in the format [[lat, lon], [lat, lon] ... etc
            variable: variable,     // which of the variables available to get timeseries data for
            time: time,             // the timestep of data chosen
            };

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