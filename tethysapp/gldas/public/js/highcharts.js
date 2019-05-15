// Global Highcharts options
Highcharts.setOptions({
    lang: {
        downloadCSV: "Download CSV",
        downloadJPEG: "Download JPEG image",
        downloadPDF: "Download PDF document",
        downloadPNG: "Download PNG image",
        downloadSVG: "Download SVG vector image",
        downloadXLS: "Download XLS",
        loading: "Loading timeseries, please wait...",
        noData: "No Data Selected"
    },
});

// Placeholder chart
let chart = Highcharts.chart('highchart', {
    title: {
        align: "center",
        text: "Your Chart Will Appear Here",
    },
    series: [{
        data: [],
    }],
    chart: {
        animation: true,
        zoomType: 'x',
        borderColor: '#000000',
        borderWidth: 2,
        type: 'area',
    },
    noData: {
        style: {
            fontWeight: 'bold',
            fontSize: '15px',
            color: '#303030'
        }
    },
});

function newHighchart(data) {
    chart = Highcharts.chart('highchart', {
        title: {
            align: "center",
            text: data['name'] + ' v Time ' + data['type'],
        },
        xAxis: {
            type: 'datetime',
            title: {text: "Time"},
        },
        yAxis: {
            title: {text: data['units']}
        },
        series: [{
            data: data['values'],
            type: "line",
            name: data['name'],
            tooltip: {
                xDateFormat: '%A, %b %e, %Y',
            },
        }],
        chart: {
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',

        },

    });
}

function getDrawnChart(drawnItems) {
    // Verify that there is a drawing on the map
    let geojson = drawnItems.toGeoJSON()['features'];
    if (geojson.length > 0) {
        chart.hideNoData();
        chart.showLoading();

        //  Compatibility if user picks something out of normal bounds
        let coords = geojson[0]['geometry']['coordinates'];
        for (let i in coords.length) {
            if (coords[i] < -180) {
                coords[i] += 360;
            }
            if (coords[i] > 180) {
                coords[i] -= 360;
            }
        }

        // setup a parameters json to generate the right timeseries
        let drawtype = geojson[0]['geometry']['type'];
        let data = {
            shptype: drawtype,
            coords: coords,
            geojson: geojson[0],
            variable: $('#variables').val(),
            time: $("#dates").val(),
            shapefile: 'false',
        };

        // call the right timeseries generator function based on type
        if (drawtype === 'Polygon') {
            $.ajax({
                url: '/apps/gldas/ajax/getPolygonAverage/',
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                method: 'POST',
                success: function (result) {
                    newHighchart(result);
                }
            })
        } else if (drawtype === 'Point') {
            $.ajax({
                url: '/apps/gldas/ajax/getPointSeries/',
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json",
                method: 'POST',
                success: function (result) {
                    newHighchart(result);
                },
            });
        }
        // If there are no drawn features, then you actually should be refreshing the shapefile chart (ie the boundary you want is the lastregion chosen)
    } else {
        getShapeChart('lastregion');
    }
}

function getShapeChart(selectedregion) {
    // if the time range is all times then confirm before executing the spatial averaging
    if ($("#dates").val() === 'alltimes') {
        if (!confirm("Computing a timeseries of spatial averages for all available times requires over 200 iterations of file conversions and geoprocessing operations. This may result in a long wait (15+ seconds) or cause errors. Are you sure you want to continue?")) {
            return
        }
    }

    drawnItems.clearLayers();
    chart.hideNoData();
    chart.showLoading();

    let data = {
        variable: $('#variables').val(),
        time: $("#dates").val(),
        shapefile: 'true',
        region: selectedregion,
    };
    if (selectedregion === 'lastregion') {
        // if we want to update, change the region to the last completed region
        data['region'] = currentregion;
    } else {
        // otherwise, the new selection is the current region on the chart
        currentregion = selectedregion;
    }

    $.ajax({
        url: '/apps/gldas/ajax/getShapeAverage/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            newHighchart(result);
        }
    })
}
