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

configs = getConfigs();     // found in ajaxFunctions.js

//  Sets the correct urls based on the time period
function setParams(configs, time, variable) {
//  Sets the links to data
    thredds_base = configs['thredds_wms_url'];
    thredds_wms = thredds_base + time + '.ncml';

//  Gets the correct bounds for the time, variable, color combination
    min_bnd = boundaries[time][variable][0];
    max_bnd = boundaries[time][variable][1];

    return thredds_wms, min_bnd, max_bnd
}


// Listeners/Controllers to let the user manipulate the map
$(document).ready(function() {

/////////////////////////////////////////////////////////////////////////////// GENERAL CONTROLS

//  Load initial map data as soon as the page is ready
    variable = $('#layers').val();
    time = $("#times").val();
    color = $('#colors').val();
    setParams(configs, time, variable);
    newLayer(variable, color);
    newControls();
    legend.addTo(map);

/////////////////////////////////////////////////////////////////////////////// LEAFLET CONTROLS

//  Listener for the variable picker menu (selectinput gizmo)
    $("#layers").change(function () {
        updateMap();
        getChart();
        });

//  Listener for the color changer
    $("#colors").change(function () {
        updateMap();
        });

//  Listener for the time selection menu
    $("#times").change(function() {
        updateMap();
        getChart();
        });

//  Listener for the opacity select slider (rangeslider gizmo)
    $("#opacity").change(function () {
        timedLayer.setOpacity($('#opacity').val());
        });

//  Listener for changing zooms
    $("#zooms").change(function() {
        zoomMap($('#zooms').val());
        });

/////////////////////////////////////////////////////////////////////////////// HIGHCHARTS CONTROLS

//  Generate a plot whenever the user draws a new point
    map.on("draw:created", function() {
        getChart();
        });

/////////////////////////////////////////////////////////////////////////////// JQUERY LISTENER

    $("#get-metrics").on("click", function() {
        getGAstats();
        });

});