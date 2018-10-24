function getChart() {
    chart.hideNoData();
    chart.showLoading();

    if (drawnItems._layers == '') {
        return
    }

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
    console.log(data);

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

