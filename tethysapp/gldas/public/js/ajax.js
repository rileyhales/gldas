function getChart() {

    chart.hideNoData();
    chart.showLoading();

//  Compatibility if user picks something out of normal bounds
    coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
    if (coords[0] < -180) {
        coords[0] += 360;
    }
    else if(coords[0] > 180) {
        coords[0] -= 360;
    }
    variable = $('#layers').val();
    time = $("#times").val();
    data = {
        coords: coords,         // list in the format [lat, lon]
        variable: variable,     // shortcode name of the variable
        time: time,             // the time interval
        };
    $.ajax({
        url:'/apps/gldas/generatePlot/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            newHighchart(result);
            },
        });
}
