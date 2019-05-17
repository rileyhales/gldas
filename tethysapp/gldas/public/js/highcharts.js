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
        noData: "No Data Selected. Place a point, draw a polygon, or select a region."
    },
});

// Placeholder chart
let histchart = Highcharts.chart('historicalchart', {
    title: {
        align: "center",
        text: "Historical Data Chart Placeholder",
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
// Statistical data chart placeholder and function
let statschart = Highcharts.chart('statisticschart', {
    title: {
        align: "center",
        text: "Statistical Analysis Chart Placeholder",
    },
    series: [{
        data: [],
    }],
    chart: {
        borderColor: '#000000',
        borderWidth: 2,
        type: 'boxplot',
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
    histchart = Highcharts.chart('historicalchart', {
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
            zoomType: 'xy',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',

        },

    });
}

function newStatisticalChart(data) {
    statschart = Highcharts.chart('statisticschart', {
        chart: {
            type: 'boxplot',
            animation: true,
            zoomType: 'xy',
            borderColor: '#000000',
            borderWidth: 2,
        },
        title: {align: "center", text: 'Monthly ' + data['name'] + ' Statistics ' + data['type']},
        legend: {enabled: false},
        xAxis: {
            type: 'datetime',
            title: {text: 'Time'},
            minTickInterval: 28 * 24 * 3600 * 1000,
        },
        yAxis: {title: {text: data['units']}},
        series: [{
            name: data['name'],
            data: data['statistics'],
            tooltip: {xDateFormat: '%b',},
        }]

    });
}

function getDrawnChart(drawnItems) {
    // Verify that there is a drawing on the map
    let geojson = drawnItems.toGeoJSON()['features'];
    if (geojson.length === 0 && currentregion === '') {
        // if theres nothing to get charts for then quit
        return
    }
    if (geojson.length > 0) {
        histchart.hideNoData();
        histchart.showLoading();
        statschart.hideNoData();
        statschart.showLoading();

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
                    newStatisticalChart(result);
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
                    newStatisticalChart(result);
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
    histchart.hideNoData();
    histchart.showLoading();
    statschart.hideNoData();
    statschart.showLoading();

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
            newStatisticalChart(result);
        }
    })
}
