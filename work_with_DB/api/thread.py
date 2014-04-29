from work_with_DB.requests import threads, posts
from work_with_DB.api.for_help import return_response, get_related_params, is_all_required_gets, get_optional_params, GET_parameters, return_error
import json
from django.http import HttpResponse


def close(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_close(id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def create(request):
    if request.method == "POST":

        request_data = json.loads(request.body)
        required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        optional = get_optional_params(request_data=request_data, optional_params=["isDeleted"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_create(forum=request_data["forum"], title=request_data["title"], isClosed=request_data["isClosed"],
                                     user=request_data["user"], date=request_data["date"], message=request_data["message"],
                                     slug=request_data["slug"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["thread"]
        related = get_related_params(request_data)
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_details(id=request_data["thread"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
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
                identificator = request_data["user"]
                entity = "user"
            except KeyError:
                return return_error("No user or forum parameters setted")
        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            t_list = threads.threads_list(entity=entity, id=identificator, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(t_list)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["thread"]
        entity = "thread"
        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            p_list = posts.post_list(entity=entity, id=request_data["thread"], related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)


def open(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_open(id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_remove(thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_restore(thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def subscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            subscription = threads.thread_subscribe(email=request_data["user"], thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def unsubscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            subscription = threads.thread_unsubscribe(email=request_data["user"], thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "slug", "message"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_update(id=request_data["thread"], slug=request_data["slug"], message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "vote"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            thread = threads.thread_vote(id=request_data["thread"], vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)