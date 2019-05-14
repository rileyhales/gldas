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
            text: data['name'] + ' v Time',
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
    // If there are no drawn features, then you actually should be refreshing the shapefile chart
    } else {
        getShapeChart();
    }
}

function getShapeChart() {
    chart.hideNoData();
    chart.showLoading();
    let data = {
        variable: $('#variables').val(),
        time: $("#dates").val(),
        shapefile: 'true',
        region: $("#regions").val(),
    };
    $.ajax({
        url: '/apps/gldas/ajax/getShapeAverage/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            console.log(result);
            newHighchart(result);
        }
    })
}
