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
function setLinks() {
    time = $("#times").val();
    variable = $('#layers').val();
    thredds_base = 'http://127.0.0.1:7000/thredds/'
    data_dir = '/home/rchales/thredds/gldas/'
    thredds_wms = thredds_base + 'wms/testAll/';
//  If you choose to show all data
    if (time == 'all') {
        thredds_wms += 'alltimes.ncml';
    }
//  Individual options for selecting a preprocessed chunk of time
    else if (time == '2000-2009') {
        thredds_wms += 'preprocessed_yrs/2000-2009/' + variable + '.nc';
    }
//  This should take care of selecting single year intervals
    else {
        thredds_wms += time + '.ncml';
    }
    return thredds_wms, time
}


// JQuery and AJAX Listeners/Controllers to let the user manipulate the map
$(document).ready(function() {

//  Load initial map data as soon as the page is ready
    variable = $('#layers').val();
    color= $('#colors').val();
    setLinks();
    newLayer(variable, color);
    getLegend(variable, color);
    newControls();

//////////////////////// GENERAL CONTROLS ///////////////////////////////////////////////

    $("#times").change(function() {
        setLinks();
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

        coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
        variable = $('#layers').val();
        data = {
            coords: coords,         // array or list in the format [[lat, lon], [lat, lon] ... etc
            variable: variable,     // which of the variables available to get timeseries data for
            time: time,             // the timestep of data chosen
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