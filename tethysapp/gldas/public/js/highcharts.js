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
chart = Highcharts.chart('highchart', {
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


function getChart(drawnItems) {
//  Compatibility if user picks something out of normal bounds
    let geometry = drawnItems.toGeoJSON()['features'];
    if (geometry.length > 0) {
        chart.hideNoData();
        chart.showLoading();

        let coords = geometry[0]['geometry']['coordinates'];
        if (coords[0] < -180) {
            coords[0] += 360;
        }
        if(coords[0] > 180) {
            coords[0] -= 360;
        }

        let data = {
            coords: coords,
            variable: $('#variables').val(),
            time: $("#dates").val(),
            };

        console.log(data);
            $.ajax({
            url:'/apps/gldas/ajax/generatePlot/',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function(result) {
                newHighchart(result);
                },
            });
    }

}