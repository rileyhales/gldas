////////////////////////////////////////////////////////////////////////  MAP FUNCTIONS
function map() {
    // create the map
    return L.map('map', {
        zoom: 2,
        minZoom: 1.25,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
        center: [20, 0],
        timeDimension: true,
        timeDimensionControl: true,
        timeDimensionControlOptions: {
            position: "bottomleft",
            autoPlay: true,
            loopButton: true,
            backwardButton: true,
            forwardButton: true,
            timeSliderDragUpdate: true,
            minSpeed: 1,
            maxSpeed: 6,
            speedStep: 1,
        },
    });
}

function basemaps() {
    // create the basemap layers
    let Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    let Esri_WorldTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {maxZoom: 13});
    let Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
    return {
        "ESRI Imagery": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(mapObj),
        "ESRI Terrain": L.layerGroup([Esri_WorldTerrain, Esri_Imagery_Labels])
    }
}

function newLayer() {
    let wmsurl = threddsbase + $("#dates").val() + '.ncml';
    let wmsLayer = L.tileLayer.wms(wmsurl, {
        // version: '1.3.0',
        layers: $("#variables").val(),
        dimension: 'time',
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/' + $('#colors').val(),
        colorscalerange: bounds[$("#dates").val()][$("#variables").val()],
    });

    let timedLayer = L.timeDimension.layer.wms(wmsLayer, {
        name: 'time',
        requestTimefromCapabilities: true,
        updateTimeDimension: true,
        updateTimeDimensionMode: 'replace',
        cache: 20,
    }).addTo(mapObj);

    return timedLayer
}

function makeControls() {
    return L.control.layers(basemapObj, {
        'GLDAS Layer': layerObj,
        'Drawing': drawnItems,
        'Europe': europe,
        'Asia': asia,
        'Middle East': middleeast,
        'North America': northamerica,
        'Central America': centralamerica,
        'South America': southamerica,
        'Africa': africa,
        'Australia': australia,
    }).addTo(mapObj);
}

function clearMap() {
    // remove the controls for the wms and wfs/geojson layers you have
    controlsObj.removeLayer(layerObj);
    controlsObj.removeLayer(africa);
    controlsObj.removeLayer(asia);
    controlsObj.removeLayer(australia);
    controlsObj.removeLayer(northamerica);
    controlsObj.removeLayer(centralamerica);
    controlsObj.removeLayer(southamerica);
    controlsObj.removeLayer(europe);
    controlsObj.removeLayer(middleeast);
    // now remove them from the map
    mapObj.removeLayer(layerObj);
    mapObj.removeLayer(africa);
    mapObj.removeLayer(asia);
    mapObj.removeLayer(australia);
    mapObj.removeLayer(northamerica);
    mapObj.removeLayer(centralamerica);
    mapObj.removeLayer(southamerica);
    mapObj.removeLayer(europe);
    mapObj.removeLayer(middleeast);
    // now delete the controls object
    mapObj.removeControl(controlsObj);
}

////////////////////////////////////////////////////////////////////////  LEGEND DEFINITIONS
let legend = L.control({position: 'topright'});
legend.onAdd = function (mapObj) {
    let div = L.DomUtil.create('div', 'legend');
    let url = threddsbase + $("#dates").val() + '.ncml' + "?REQUEST=GetLegendGraphic&LAYER=" + $("#variables").val() + "&PALETTE=" + $('#colors').val() + "&COLORSCALERANGE=" + bounds[$("#dates").val()][$("#variables").val()];
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};

////////////////////////////////////////////////////////////////////////  GEOJSON LAYERS - GEOSERVER + WFS
let currentregion;
function layerPopups(feature, layer) {
    layer.bindPopup('<a class="btn btn-default" role="button" onclick="getShapeChart()">Get timeseries of averages for ' + feature.properties.name + '</a>')
}
let africa = L.geoJSON(false, {onEachFeature: layerPopups});
let asia = L.geoJSON(false, {onEachFeature: layerPopups});
let australia = L.geoJSON(false, {onEachFeature: layerPopups});
let centralamerica = L.geoJSON(false, {onEachFeature: layerPopups});
let europe = L.geoJSON(false, {onEachFeature: layerPopups});
let middleeast = L.geoJSON(false, {onEachFeature: layerPopups});
let northamerica = L.geoJSON(false, {onEachFeature: layerPopups});
let southamerica = L.geoJSON(false, {onEachFeature: layerPopups});

function getWFSData(geoserverlayer, leafletlayer) {
    // http://jsfiddle.net/1f2Lxey4/2/
    let parameters = L.Util.extend({
        service: 'WFS',
        version: '1.0.0',
        request: 'GetFeature',
        typeName: 'gldas:' + geoserverlayer,
        maxFeatures: 10000,
        outputFormat: 'application/json',
        parseResponse: 'getJson',
        srsName: 'EPSG:4326',
        crossOrigin: 'anonymous'
    });
    $.ajax({
        async: true,
        jsonp: false,
        url: geoserverbase + L.Util.getParamString(parameters),
        contentType: 'application/json',
        jsonpCallback: 'getJson',  // name of the function to fire on jsonpCallback
        success: function (data) {
            leafletlayer.addData(data); //.addTo(mapObj);
        },
    });
}

function updateGEOJSON() {
    getWFSData('africa', africa);
    getWFSData('asia', asia);
    getWFSData('australia', australia);
    getWFSData('centralamerica', centralamerica);
    getWFSData('europe', europe);
    getWFSData('middleeast', middleeast);
    getWFSData('northamerica', northamerica);
    getWFSData('southamerica', southamerica);
}

////////////////////////////////////////////////////////////////////////  GEOJSON LAYERS - LOCAL JS FILES
/*
let africa = L.geoJSON(false, {onEachFeature: layerPopups});
let asia = L.geoJSON(false, {onEachFeature: layerPopups});
let australia = L.geoJSON(false, {onEachFeature: layerPopups});
let centralamerica = L.geoJSON(false, {onEachFeature: layerPopups});
let europe = L.geoJSON(false, {onEachFeature: layerPopups});
let middleeast = L.geoJSON(false, {onEachFeature: layerPopups});
let northamerica = L.geoJSON(false, {onEachFeature: layerPopups});
let southamerica = L.geoJSON(false, {onEachFeature: layerPopups});
 */