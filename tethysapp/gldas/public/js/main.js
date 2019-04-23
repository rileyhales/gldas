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


$(document).ready(function() {
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
        return L.control.layers(basemapObj, {'GLDAS Layer': layerObj, 'Point': drawnItems}).addTo(mapObj);
    }

    function clearMap() {
        controlsObj.removeLayer(layerObj);
        mapObj.removeLayer(layerObj);
        mapObj.removeControl(controlsObj);
    }

    ////////////////////////////////////////////////////////////////////////  AJAX FUNCTIONS
    function getThreddswms() {
        $.ajax({
            url:'/apps/gldas/ajax/customsettings/',
            async: false,
            data: '',
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function(result) {
                wmsbase = result['threddsurl'];
                return wmsbase;
                },
            });
        return wmsbase;
    }

    ////////////////////////////////////////////////////////////////////////  INITIALIZE MAP ON DOCUMENT READY
    //  Load initial map data as soon as the page is ready
    var wmsbase = getThreddswms();
    var mapObj = map();

    ////////////////////////////////////////////////////////////////////////  SETUP FOR LEGEND AND DRAW CONTROLS
    let legend = L.control({position:'bottomright'});
        legend.onAdd = function(mapObj) {
            let div = L.DomUtil.create('div', 'legend');
            let url = wmsbase + $("#dates").val() + '.ncml' + "?REQUEST=GetLegendGraphic&LAYER=" + $("#variables").val() + "&PALETTE=" + $('#colors').val() + "&COLORSCALERANGE=" + bounds[$("#dates").val()][$("#variables").val()];
            div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
            return div
        };
    legend.addTo(mapObj);

    // Add controls for user drawings
    var drawnItems = new L.FeatureGroup().addTo(mapObj);      // FeatureGroup is to store editable layers
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
    mapObj.addControl(drawControl);
    mapObj.on("draw:drawstart ", function () {     // control what happens when the user draws things on the map
        drawnItems.clearLayers();
    });

    mapObj.on(L.Draw.Event.CREATED, function (event) {
        drawnItems.addLayer(event.layer);
        L.Draw.Event.STOP;
        getChart(drawnItems);
        // e.layer.addTo(drawnItems);
    });

    var basemapObj = basemaps();
    var layerObj = newLayer();
    var controlsObj = makeControls();


    ////////////////////////////////////////////////////////////////////////  EVENT LISTENERS

    //  Listener for the variable picker menu (selectinput gizmo)
    $("#dates").change(function () {
        clearMap();
        layerObj = newLayer();
        controlsObj = makeControls();
        legend.addTo(mapObj);
    });

    $("#variables").change(function () {
        clearMap();
        layerObj = newLayer();
        controlsObj = makeControls();
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

});
