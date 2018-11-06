import pprint, ast
from resources import app_configuration
from django.http import JsonResponse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

"""Hello Analytics Reporting API V4."""

def init_analytics(key_location, scopes):
    """
    Initializes and Returns An authorized
    Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_location, scopes)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, viewID, metrics):
    """Queries the Analytics Reporting API V4.
    Args:
    analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
    The Analytics Reporting API V4 response.
    """
    reports = analytics.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': viewID,
                'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                'metrics': metrics,
                'dimensions': [{'name': 'ga:country'}]
                }]
            }
        ).execute()

    pprint.pprint(reports)
    return reports


def print_results(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    results = {}

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                results[header] = dimension

            for i, values in enumerate(dateRangeValues):
                results['Date range' + str(i)] = str(i)
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    results[metricHeader.get('name')] = value

    print(results)
    return results


def GAstats(request):
    data = ast.literal_eval(request.body)['metrics']
    pprint.pprint(data)
    metrics = []
    for metric in data:
        tmp = {'expression': metric}
        metrics.append(tmp)

    app_config = app_configuration()
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    key_location = app_config['app_wksp_path'] + 'api_info.json'
    viewID = app_config['viewID']

    analytics = init_analytics(key_location, scopes)
    response = get_report(analytics, viewID, metrics)
    results = print_results(response)

    return JsonResponse(results)
