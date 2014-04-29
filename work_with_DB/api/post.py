from work_with_DB.requests import posts
import json
from django.http import HttpResponse
from work_with_DB.api.for_help import is_all_required_gets, return_response, get_optional_params, get_related_params, GET_parameters, return_error


def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "forum", "thread", "message", "date"]
        optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        optional = get_optional_params(request_data=request_data, optional_params=optional_data)
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_create(date=request_data["date"], thread=request_data["thread"],
                                message=request_data["message"], user=request_data["user"],
                                forum=request_data["forum"], optional_params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":

        request_data = GET_parameters(request)
        required_data = ["post"]
        related = get_related_params(request_data)
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_details(request_data["post"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def list(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        identificator = None
        try:
            identificator = request_data["forum"]
            entity = "forum"
        except KeyError:
            try:
                identificator = request_data["thread"]
                entity = "thread"
            except KeyError:
                return return_error("No thread or forum parameters in request")

        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            p_list = posts.post_list(entity=entity, id=identificator, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_remove(post_id=request_data["post"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_restore(post_id=request_data["post"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "message"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_update(id=request_data["post"], message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "vote"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            post = posts.post_vote(id=request_data["post"], vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)