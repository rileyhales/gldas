function newChart() {
    chart.hideNoData();
    chart.showLoading();

    coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
    variable = $('#layers').val();
    time = $("#times").val();
    data = {
        coords: coords,         // array or list in the format [[lat, lon], [lat, lon] ... etc
        variable: variable,     // which of the variables available to get timeseries data for
        time: time,             // the timestep of data chosen
        };

// Ajax script to send the data for processing
    $.ajax({
        url:'/apps/gldas/generatePlot/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            console.log(result);
            newHighchart(result);
            },
        });

}


function getBounds() {
    variable = $('#layers').val();
    time = $("#times").val();
    data = {
        variable: variable,
        time: time,
        };

    $.ajax({
        async: false,
        url:'/apps/gldas/getBounds/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            console.log(result);
            data_min = result['minimum'];
            data_max = result['maximum'];
            return data_min, data_max
            },
        });

    return data_min, data_max
}

