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

////////////////////////////////////////////////////////////////////////  LOAD THE MAP
// threddsbase and geoserverbase and model are defined in the base.html scripts sections
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function

////////////////////////////////////////////////////////////////////////  DRAWING/LAYER CONTROLS, MAP EVENTS, LEGEND
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

mapObj.on("mousemove", function (event) {
    $("#mouse-position").html('Lat: ' + event.latlng.lat.toFixed(5) + ', Lon: ' + event.latlng.lng.toFixed(5));
});

let layerObj = newLayer();              // adds the wms raster layer
let controlsObj = makeControls();       // the layer toggle controls top-right corner
legend.addTo(mapObj);                   // add the legend graphic to the map
latlon.addTo(mapObj);                   // add the box showing lat and lon to the map
addGEOJSON();                           // add the geojson world boundary regions

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
function update() {
    for (let i in geojsons) {
        geojsons[i].addTo(mapObj)
    }
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
}
// data controls
$("#variables").change(function () {clearMap();update();getDrawnChart(drawnItems);});
$("#dates").change(function () {clearMap();update();getDrawnChart(drawnItems);});
$("#use_dates").change(function () {customdates()});
$('#charttype').change(function () {makechart();});
$("#levels").change(function () {clearMap();update();});
// display controls
$("#display").click(function() {$("#displayopts").toggle();});
$("#use_csrange").change(function () {clearMap();update()});
$('#colorscheme').change(function () {clearMap();update();});
$("#opacity").change(function () {layerObj.setOpacity($(this).val())});
$('#gjClr').change(function () {styleGeoJSON();});
$("#gjOp").change(function () {styleGeoJSON();});
$("#gjWt").change(function () {styleGeoJSON();});
$('#gjFlClr').change(function () {styleGeoJSON();});
$("#gjFlOp").change(function () {styleGeoJSON();});
