// see base.html scripts for thredds, geoserver, app, model, instance_id
let csrftoken = Cookies.get('csrftoken');
Cookies.set('instance_id', instance_id);

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

mapObj.on("mousemove", function (event) {$("#mouse-position").html('Lat: ' + event.latlng.lat.toFixed(5) + ', Lon: ' + event.latlng.lng.toFixed(5));});

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
    usershape.addTo(mapObj);
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
}
function changeInputs() {
    let charts = $("#charttype");
    charts.empty();
    charts.append('<option value="timeseries">Full Timeseries (Single-Line Plot)</option>');
    if ($("#dates").val() === 'alltimes') {
        charts.append('<option value="monthbox">Monthly Analysis (Box Plot)</option>' +
            '<option value="monthmulti">Monthly Analysis (Multi-Line Plot)</option>' +
            '<option value="yearbox">Yearly Analysis (Box Plot)</option>' +
            '<option value="yearmulti">Yearly Analysis (Multi-Line Plot)</option>');
    }
    charts.val('timeseries');
}
$(".customs").keyup(function () {this.value = this.value.replace(/i[a-z]/, '')});

// data controls
$("#variables").change(function () {clearMap();update();getDrawnChart(drawnItems);});
$("#dates").change(function () {changeInputs();clearMap();update();getDrawnChart(drawnItems);});
$('#charttype').change(function () {makechart();});
$("#levels").change(function () {clearMap();update();});

// display controls
$("#display").click(function() {$("#displayopts").toggle();});
$("#cs_min").change(function () {if ($("#use_csrange").is(":checked")) {clearMap();update()}});
$("#cs_max").change(function () {if ($("#use_csrange").is(":checked")) {clearMap();update()}});
$("#use_csrange").change(function () {clearMap();update()});
// $("#use_times").change(function () {customdates()});
$('#colorscheme').change(function () {clearMap();update();});
$("#opacity").change(function () {layerObj.setOpacity($(this).val())});
$('#gjClr').change(function () {styleGeoJSON();});
$("#gjOp").change(function () {styleGeoJSON();});
$("#gjWt").change(function () {styleGeoJSON();});
$('#gjFlClr').change(function () {styleGeoJSON();});
$("#gjFlOp").change(function () {styleGeoJSON();});