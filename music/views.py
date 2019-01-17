from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from database.gstore import GstoreConnector


# Create your views here.
def index(request):
    return render(request, "music/index.html")


def query(request):
    sparql = request.GET['sparql']
    gc = GstoreConnector('*', 1, '*', '*')
    response = gc.query('music', sparql)
    bindings = response['results']['bindings']
    print(response['StatusCode'], bindings)
    result = []
    for item in bindings:
        for var_name in item.keys():
            attrs = item[var_name]
            result.append('{}: {}'.format(var_name, attrs['value']))
    return JsonResponse({'result':result})
