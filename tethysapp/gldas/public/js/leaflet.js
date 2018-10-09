// creating the map
var map = L.map('map', {
    zoom: 2,
    fullscreenControl: true,
    timeDimension: true,
    center: [20, 0],
});


// create the basemap layers (default basemap is world imagery)
var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}').addTo(map);
var Esri_WorldTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {maxZoom: 13});
var openStreetMap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
   attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
   name: 'openStreetMap',
    });


// Add controls for user drawings
var drawnItems = new L.FeatureGroup();      // FeatureGroup is to store editable layers
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false,
    },
    draw: {
        polyline: false,
        circlemarker:false,
        circle:false,
        polygon:false,
        rectangle:false,
    },
});
map.addControl(drawControl);


// Listeners that control what happens when the user draws things on the map
map.on("draw:drawstart ", function (e) {
    drawnItems.clearLayers();
});
map.on("draw:created", function (e) {
    var layer = e.layer;
    layer.addTo(drawnItems);
});


function newLayer(variable, color) {
    url = thredds_wms_url + variable + ".nc"
    wmsLayer = L.tileLayer.wms(url, {
        layers: variable,
        format: 'image/png',
        transparent: true,
        BGCOLOR:'0x000000',
        opacity: $("#opacity").val(),
        styles: 'boxfill/' + color,
        legend: true,
        colorscalerange: '215,325'
        });

    timedLayer = L.timeDimension.layer.wms(wmsLayer, {
        updateTimeDimension: true,
        name: 'TimeSeries',
        }).addTo(map);
}


function getLegend(variable, color) {
    url = thredds_wms_url + variable + ".nc"
    legendUrl = url + "?REQUEST=GetLegendGraphic&LAYER=" + variable + "&PALETTE=" + color;
    legendUrl += "&COLORSCALERANGE=215,325"
    lookup = '<img src="' + legendUrl + '" alt="legend" style="width:100%; float:right;">'
    document.getElementById("legend").innerHTML = lookup;
}


// removes old controls and adds new ones. Must be called after changeLayer
function newControls(basemaps) {
    sliderControl = L.control.timeDimension({
        position: "bottomleft",
        layer: timedLayer,
        range: true,
        autoPlay: false,
        });
    data_layers = {
        'GLDAS Layer': timedLayer,
        }
    basemaps = {
    "ESRI Imagery": Esri_WorldImagery,
    "ESRI Terrain": Esri_WorldTerrain,
    "OpenStreetMap": openStreetMap,
        }
    layer_controller = L.control.layers(basemaps, data_layers).addTo(map);
    map.addControl(sliderControl);
}


function rmControls() {
    layer_controller.removeLayer(timedLayer);
    map.removeControl(layer_controller)
    map.removeControl(sliderControl);
}


function updateMap() {
    variable = $('#layers').val();
    color= $('#colors').val();
    map.removeLayer(wmsLayer);
    newLayer(variable, color);
    rmControls();
    newControls();
    getLegend(variable, color);
}
