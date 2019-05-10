let bnds_africa;
let bnds_asia;
let bnds_australia;
let bnds_central;
let bnds_europe;
let bnds_mideast;
let bnds_north;
let bnds_south;

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
    let wmsurl = wmsbase + $("#dates").val() + '.ncml';
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
    return L.control.layers(basemapObj,
        {'GLDAS Layer': layerObj,
            'Drawing': drawnItems,
            'Europe': bnds_europe,
            'Asia': bnds_asia,
            'Middle East': bnds_mideast,
            'North America': bnds_north,
            'Central America': bnds_central,
            'South America': bnds_south,
            'Africa': bnds_africa,
            'Australia': bnds_australia,
        }).addTo(mapObj);
}

function addcontinents() {
    bnds_africa = L.geoJSON(africa);
    bnds_asia = L.geoJSON(asia);
    bnds_australia = L.geoJSON(australia);
    bnds_north = L.geoJSON(northamerica);
    bnds_central = L.geoJSON(centralamerica);
    bnds_south = L.geoJSON(southamerica);
    bnds_europe = L.geoJSON(europe);
    bnds_mideast = L.geoJSON(mideast);
    return
}

function clearMap() {
    controlsObj.removeLayer(layerObj);
    controlsObj.removeLayer(bnds_africa);
    controlsObj.removeLayer(bnds_asia);
    controlsObj.removeLayer(bnds_australia);
    controlsObj.removeLayer(bnds_north);
    controlsObj.removeLayer(bnds_central);
    controlsObj.removeLayer(bnds_south);
    controlsObj.removeLayer(bnds_europe);
    controlsObj.removeLayer(bnds_mideast);
    mapObj.removeLayer(layerObj);
    mapObj.removeLayer(bnds_africa);
    mapObj.removeLayer(bnds_asia);
    mapObj.removeLayer(bnds_australia);
    mapObj.removeLayer(bnds_north);
    mapObj.removeLayer(bnds_central);
    mapObj.removeLayer(bnds_south);
    mapObj.removeLayer(bnds_europe);
    mapObj.removeLayer(bnds_mideast);
    mapObj.removeControl(controlsObj);
}