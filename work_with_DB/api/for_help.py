import json
from django.http import HttpResponse

def get_related_params(request_data):
    try:
        related = request_data["related"]
    except KeyError:
        related = []
    return related


def get_optional_params(request_data, optional_params):
    optional = {}
    for param in optional_params:
        try:
            optional[param] = request_data[param]
        except KeyError:
            continue
    return optional


def GET_parameters(request_data):
    data = {}
    for el in request_data.GET:
        data[el] = request_data.GET.get(el)
    return data


def return_response(object):
    response_data = {"code": 0, "response": object}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def return_error(message):
    response_data = {"code": 1, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def is_all_required_gets(params, required):
    for el in required:
        if el not in params:
            raise Exception("required element " + el + " not in parameters")
        if params[el] is not None:
            try:
                params[el] = params[el].encode('utf-8')
            except Exception:
                continue

    return