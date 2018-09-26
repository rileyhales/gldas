$(document).ready(function() {
    // Ajax sends the coordinates of the user's drawing and gets back a plot of the data at the given point/area
    $("#generatePlot").click(function () {
    //        validate that the user has provided the right information
        try {
            coords = drawnItems.toGeoJSON()['features'][0]['geometry']['coordinates'];
        }
        catch {
            alert("Please select a region before generating a timeseries.");
            console.log("failed to generate timeseries: no area selected")
            return;
        }
        variable = $('#select1').val();
        if(variable == "") {
            alert("Please Select a variable before generating a timeseries.");
            console.log("failed to generate timeseries: no variable selected")
            return;
        };
        data = {
            coords: coords,     // array or list in the format [[lat, lon], [lat, lon] ... etc
            variable: variable, // which of the variables available to get timeseries data for
        };

        console.log(data)

    //        Ajax script to send the data for processing
        $.ajax({
            url:'/apps/gldas/generatePlot/',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function(result) {
                console.log(result);
                Highcharts.chart('highchart', {
                    title: {
                        align: "center",
                        text: "Timeseries for " + $('#select1').val().toString(),
                    },
                    series: [{
                        data: result['values'],
                    }],
                    legend: [{
                        enabled: false,
                    }],
                });
            },
        });
    });

});