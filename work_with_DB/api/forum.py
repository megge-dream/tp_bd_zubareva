from work_with_DB.requests import forums, posts, threads
from work_with_DB.api.for_help import *
import json
from django.http import HttpResponse

def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["name", "short_name", "user"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            forum = forums.forum_create(name=request_data["name"], short_name=request_data["short_name"],
                                      user=request_data["user"])
        except Exception as e:
            print("name = " + request_data["name"])
            print("short_name = " + request_data["short_name"])
            print("user = " + request_data["user"])
            print(e.message)
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related_params(request_data)
        try:
            is_all_required_gets(params=request_data, required=required_data)
            forum = forums.forum_details(short_name=request_data["forum"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related_params(request_data)

        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            current_list_posts = posts.post_list(entity="forum", id=request_data["forum"],
                                       related=related, params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(current_list_posts)
    else:
        return HttpResponse(status=400)


def list_threads(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related_params(request_data)
        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            current_list_threads = threads.threads_list(entity="forum", id=request_data["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(current_list_threads)
    else:
        return HttpResponse(status=400)


def list_users(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since_id"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            current_list_users = forums.forum_list_users(request_data["forum"], optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(current_list_users)
    else:
        return HttpResponse(status=400)