// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


////////////////////////////////////////////////////////////////////////  AJAX FUNCTIONS
function getThreddswms() {
    $.ajax({
        url: '/apps/gldas/ajax/customsettings/',
        async: false,
        data: '',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            threddsbase = result['threddsurl'];
            geoserverbase = result['geoserverurl']
        },
    });
}

////////////////////////////////////////////////////////////////////////  LOAD THE MAP
//  Load initial map data as soon as the page is ready
let threddsbase;
let geoserverbase;
getThreddswms();                        // sets the value of threddsbase and geoserverbase
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function

////////////////////////////////////////////////////////////////////////  DRAWING/LAYER CONTROLS, LEGEND
let drawnItems = new L.FeatureGroup().addTo(mapObj);      // FeatureGroup is to store editable layers
let drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false,
    },
    draw: {
        polyline: false,
        circlemarker: false,
        circle: false,
        polygon: false,
        rectangle: true,
    },
});
mapObj.addControl(drawControl);
mapObj.on("draw:drawstart ", function () {     // control what happens when the user draws things on the map
    drawnItems.clearLayers();
});
mapObj.on(L.Draw.Event.CREATED, function (event) {
    drawnItems.addLayer(event.layer);
    L.Draw.Event.STOP;
    getDrawnChart(drawnItems);
});

let layerObj = newLayer();              // adds the wms raster layer
let controlsObj = makeControls();       // the layer toggle controls top-right corner
legend.addTo(mapObj);                   // add the legend graphic to the map
updateGEOJSON();                        // asynchronously get geoserver wfs data for the regions

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
$("#dates").change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    getDrawnChart(drawnItems);
    legend.addTo(mapObj);
});

$("#variables").change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    getDrawnChart(drawnItems);
    legend.addTo(mapObj);
});

$("#opacity").change(function () {
    layerObj.setOpacity($('#opacity').val());
});

$('#colors').change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
});

$("#shpaverage").click(function () {
    if ($("#dates").val() === 'alltimes') {
        if (confirm("Computing a timeseries of spatial average data requires over 200 iterations of file conversions and geoprocessing operations. This may result in a long wait (about 20 seconds) or cause errors. Are you sure you want to continue?")) {
            drawnItems.clearLayers();
            getShapeChart();
        }
    } else {
        drawnItems.clearLayers();
        getShapeChart();
    }
});