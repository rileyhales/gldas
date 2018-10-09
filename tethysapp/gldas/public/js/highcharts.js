// Global Highcharts options
Highcharts.setOptions({
    lang: {
        downloadCSV: "Download CSV",
        downloadJPEG: "Download JPEG image",
        downloadPDF: "Download PDF document",
        downloadPNG: "Download PNG image",
        downloadSVG: "Download SVG vector image",
        downloadXLS: "Download XLS",
        loading: "Loading...",
        noData: "No Timeseries Data Selected",
    },
});

// Place holder chart
Highcharts.chart('highchart', {
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
            text: "Timeseries for " + data['name'],
        },
        series: [{
            data: data['values'],
            type: "line",
            name: data['name'],
        }],
        chart: {
            animation: true,
            zoomType: 'x',
        },
    });
}
