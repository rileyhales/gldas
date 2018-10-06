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
basemaps = {
    "ESRI Imagery": Esri_WorldImagery,
    "ESRI Terrain": Esri_WorldTerrain,
    "OpenStreetMap": openStreetMap,
}

layer_controller = L.control.layers(basemaps).addTo(map);

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

threddsURL = "http://127.0.0.1:7000/thredds/wms/testAll/Swnet_tavg.nc";
function changeLayer(variable) {
    try {
        map.removeLayer(wmsLayer);
    }
    catch {
        console.log("no layers to remove")
    }
    finally {
        wmsLayer = L.tileLayer.wms(threddsURL, {
            layers: 'Swnet_tavg',
            format: 'image/png',
            transparent: true,
            opacity: $("#slider1").val(),
            styles: 'boxfill/prob',
            legend: true,
            });

        timedLayer = L.timeDimension.layer.wms(wmsLayer, {
            updateTimeDimension: true,
            name: 'TimeSeries',
            }).addTo(map);
    }
}

// removes old controls and adds new ones. Must be called after changeLayer
function updateControls() {
    try {
        map.removeControl(layer_controller);
        map.removeControl(sliderControl);
        }
    catch {
        console.log("no controls to remove")
    }
    finally {
    sliderControl = L.control.timeDimension({
        position: "bottomleft",
        layer: timedLayer,
        range: true,
        autoPlay: false,
        });
    data_layers = {
        'GLDAS Layer': timedLayer,
        }
    layer_controller = L.control.layers(basemaps, data_layers).addTo(map);
    map.addControl(sliderControl);
    }
}

// remove layers and related controls
function removeData() {
    try {
        layer_controller.removeLayer(timedLayer);
        map.removeLayer(timedLayer)
        map.removeControl(sliderControl);
        console.log("Variable layers cleared");
    }
    catch {
        console.log("No variable layers to remove")
    }
    finally {
        drawnItems.clearLayers();
        console.log("Drawn items cleared");
    }
}


// JQuery and AJAX Listeners/Controllers to let the user manipulate the map
$(document).ready(function() {

//    Listener for the variable picker menu (selectinput gizmo)
    $("#select1").change(function () {
        changeLayer($('#select1').val());
        updateControls();
        });

//    Listener for the opacity select slider (rangeslider gizmo)
    $("#slider1").change(function () {
        try {
            timedLayer.setOpacity($('#slider1').val());
        }
        catch {
            console.log("No layer opacity to change")
        }
        });

//    Listener for the remove layers button (html button)
    $("#removal").click(function () {
        removeData()
        });

});
