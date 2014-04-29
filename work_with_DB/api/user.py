from work_with_DB.requests import users, posts
from work_with_DB.api.for_help import return_response, is_all_required_gets, get_optional_params, GET_parameters, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["email", "username", "name", "about"]
        optional = get_optional_params(request_data=request_data, optional_params=["isAnonymous"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            user = users.user_create(email=request_data["email"], username=request_data["username"],
                               about=request_data["about"], name=request_data["name"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            user_details = users.user_details(email=request_data["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user_details)
    else:
        return HttpResponse(status=400)


def follow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            following = users.user_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=400)


def list_followers(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        followers_param = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since_id"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            follower_l = users.user_list_followers_or_following(email=request_data["user"], type="follower", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(follower_l)
    else:
        return HttpResponse(status=400)


def list_following(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        followers_param = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since_id"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            followings = users.user_list_followers_or_following(email=request_data["user"], type="followee", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(followings)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        optional = get_optional_params(request_data=request_data, optional_params=["limit", "order", "since"])
        try:
            is_all_required_gets(params=request_data, required=required_data)
            posts_l = posts.post_list(entity="user", id=request_data["user"], related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=400)


def unfollow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            following = users.user_unfollow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=400)


def update_profile(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "name", "about"]
        try:
            is_all_required_gets(params=request_data, required=required_data)
            user = users.user_update_profile(email=request_data["user"], name=request_data["name"], about=request_data["about"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=400)