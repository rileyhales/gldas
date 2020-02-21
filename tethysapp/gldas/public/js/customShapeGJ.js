let uploaded_shapefile = false;
let uploaded_geojson = false;

function uploadShapefile() {
    let files = $('#shapefile-upload')[0].files;

    if (files.length !== 4) {
        alert('The files you selected were rejected. Upload exactly 4 files ending in shp, shx, prj and dbf.');
        return
    }

    let data = new FormData();
    Object.keys(files).forEach(function (file) {
        data.append('files', files[file]);
    });

    let loadgif = $("#loading");
    loadgif.show();
    $.ajax({
        url: '/apps/' + app + '/ajax/uploadShapefile/',
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function (response) {
            uploaded_shapefile = true;
            loadgif.hide();
            // $("#geometry-modal").modal('hide');
            getGeoServerGJ(response['gsworksp'], response['shpname'], response['gsurl']);
        },
    });
}

// todo
// function uploadGeoJSON() {
//     let files = $('#geojson-upload')[0].files;
//
//     if (files.length !== 1) {
//         alert('The files you selected were rejected. Upload exactly 1 files ending in .geojson or .json');
//         return
//     }
//
//     let data = new FormData();
//     Object.keys(files).forEach(function (file) {
//         data.append('files', files[file]);
//     });
//
//     let loadgif = $("#loading");
//     loadgif.show();
//     $.ajax({
//         url: '/apps/' + app + '/ajax/uploadGeoJSON/',
//         type: 'POST',
//         data: data,
//         dataType: 'json',
//         processData: false,
//         contentType: false,
//         success: function (response) {
//             uploaded_geojson = true;
//             loadgif.hide();
//             // $("#geometry-modal").modal('hide');
//             user_geojson.clearLayers();
//             mapObj.removeLayer(drawnItems);
//             user_geojson.addData(data).addTo(mapObj);
//             styleGeoJSON();
//             mapObj.flyToBounds(user_geojson.getBounds());
//         },
//     });
// }

$("#uploadshp").click(function () {uploadShapefile();});
$("#uploadgj").click(function () {uploadGeoJSON();});

$("#customShpChart").click(function () {
    if (uploaded_shapefile) {
        getShapeChart('Shapefile')
    } else {
        if (confirm('You need to upload a shapefile before using this function. Would you like to upload some data?')){
            $("#geometry-modal").modal('show');
        }
    }
});
$("#customGjChart").click(function () {
    if (uploaded_geojson) {
        getShapeChart('GeoJSON')
    } else {
        if (confirm('You need to upload a geojson before using this function. Would you like to upload some data?')){
            $("geometry-modal").modal('show');
        }
    }
});