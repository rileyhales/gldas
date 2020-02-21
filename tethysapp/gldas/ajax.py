import ast
import os
import zipfile
import subprocess
import json
import shutil
import geomatics as gm

from django.http import JsonResponse

from .charts import newchart
from .app import Gldas as App


def getchart(request):
    data = ast.literal_eval(request.body.decode('utf-8'))
    data['instance_id'] = request.META['HTTP_COOKIE'].split('instance_id=')[1][0:9]
    data['stats'] = True
    return JsonResponse(newchart(data))


def uploadshapefile(request):
    files = request.FILES.getlist('files')
    instance_id = request.META['HTTP_COOKIE'].split('instance_id=')[1][0:9]
    user_workspace = os.path.join(os.path.dirname(__file__), 'workspaces', 'user_workspaces', instance_id)
    if not os.path.exists(user_workspace):
        os.mkdir(user_workspace)

    # write the new files to the directory
    for n, file in enumerate(files):
        with open(os.path.join(user_workspace, file.name), 'wb') as dst:
            for chunk in files[n].chunks():
                dst.write(chunk)

    # check that the user has provided geoserver settings
    gs_eng = App.get_spatial_dataset_service(name='geoserver', as_engine=True)
    gs_wfs = App.get_spatial_dataset_service(name='geoserver', as_wfs=True)
    gs_store = 'user-uploads:' + instance_id
    shp = [i for i in os.listdir(user_workspace) if i.endswith('.shp')][0].split('.')[0]
    shppath = os.path.join(user_workspace, shp)
    gs_eng.create_shapefile_resource(
        store_id=gs_store,
        shapefile_base=shppath,
        overwrite=True
        )

    # rename the files and create a zip archive
    files = os.listdir(user_workspace)
    zippath = os.path.join(user_workspace, instance_id + '.zip')
    archive = zipfile.ZipFile(zippath, mode='w')
    for file in files:
        archive.write(os.path.join(user_workspace, file), arcname=file)
    archive.close()

    # upload the archive to geoserver
    shellpath = os.path.join(App.get_app_workspace().path, 'upload_shapefile.sh')
    v1 = gs_eng.username
    v2 = gs_eng.password
    v3 = zippath
    v4 = gs_eng.endpoint
    v5 = App.package
    v6 = shp
    subprocess.call(['bash', shellpath, v1, v2, v3, v4, v5, v6])

    return JsonResponse({'gsurl': gs_wfs, 'gsworksp': v5, 'shpname': v6})


def uploadgeojson(request):
    files = request.FILES.getlist('files')
    instance_id = request.META['HTTP_COOKIE'].split('instance_id=')[1][0:9]
    user_workspace = os.path.join(os.path.dirname(__file__), 'workspaces', 'user_workspaces', instance_id)
    if not os.path.exists(user_workspace):
        os.mkdir(user_workspace)
    gj_file_path = os.path.join(user_workspace, 'usergj.geojson')

    # write the new files to the directory
    for n, file in enumerate(files):
        with open(gj_file_path, 'wb') as dst:
            for chunk in files[n].chunks():
                dst.write(chunk)

    try:
        with open(gj_file_path, 'r') as gj:
            gm.geojsons.geojson_to_shp(json.loads(gj.read()), os.path.join(user_workspace, 'usergj.shp'))
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failed'})

    return JsonResponse({'status': 'succeeded'})
