from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^db/api/clear$', 'work_with_DB.requests.clear.dropDB', name='drop_forum'),
    # Forum
    url(r'^db/api/forum/create/$', 'work_with_DB.api.forum.create', name='create_forum'),
    url(r'^db/api/forum/details/$', 'work_with_DB.api.forum.details', name='details_forum'),
    url(r'^db/api/forum/listThreads/$', 'work_with_DB.api.forum.list_threads', name='listThreads_forum'),
    url(r'^db/api/forum/listPosts/$', 'work_with_DB.api.forum.list_posts', name='listPosts_forum'),
    url(r'^db/api/forum/listUsers/$', 'work_with_DB.api.forum.list_users', name='listUsers_forum'),

    # Post
    url(r'^db/api/post/create/$', 'work_with_DB.api.post.create', name='create_post'),
    url(r'^db/api/post/details/$', 'work_with_DB.api.post.details', name='details_post'),
    url(r'^db/api/post/list/$', 'work_with_DB.api.post.list', name='list_post'),
    url(r'^db/api/post/remove/$', 'work_with_DB.api.post.remove', name='remove_post'),
    url(r'^db/api/post/restore/$', 'work_with_DB.api.post.restore', name='restore_post'),
    url(r'^db/api/post/update/$', 'work_with_DB.api.post.update', name='update_post'),
    url(r'^db/api/post/vote/$', 'work_with_DB.api.post.vote', name='vote_post'),

    # User
    url(r'^db/api/user/create/$', 'work_with_DB.api.user.create', name='create_user'),
    url(r'^db/api/user/details/$', 'work_with_DB.api.user.details', name='details_user'),
    url(r'^db/api/user/follow/$', 'work_with_DB.api.user.follow', name='follow_user'),
    url(r'^db/api/user/unfollow/$', 'work_with_DB.api.user.unfollow', name='unfollow_user'),
    url(r'^db/api/user/listFollowers/$', 'work_with_DB.api.user.list_followers', name='list_followers'),
    url(r'^db/api/user/listFollowing/$', 'work_with_DB.api.user.list_following', name='list_following'),
    url(r'^db/api/user/updateProfile/$', 'work_with_DB.api.user.update_profile', name='update_user'),
    url(r'^db/api/user/listPosts/$', 'work_with_DB.api.user.list_posts', name='posts_user'),

    # Thread
    url(r'^db/api/thread/create/$', 'work_with_DB.api.thread.create', name='create_thread'),
    url(r'^db/api/thread/details/$', 'work_with_DB.api.thread.details', name='details_thread'),
    url(r'^db/api/thread/subscribe/$', 'work_with_DB.api.thread.subscribe', name='subscribe_thread'),
    url(r'^db/api/thread/unsubscribe/$', 'work_with_DB.api.thread.unsubscribe', name='unsubscribe_thread'),
    url(r'^db/api/thread/open/$', 'work_with_DB.api.thread.open', name='open_thread'),
    url(r'^db/api/thread/close/$', 'work_with_DB.api.thread.close', name='close_thread'),
    url(r'^db/api/thread/vote/$', 'work_with_DB.api.thread.vote', name='vote_thread'),
    url(r'^db/api/thread/list/$', 'work_with_DB.api.thread.list', name='list_thread'),
    url(r'^db/api/thread/update/$', 'work_with_DB.api.thread.update', name='update_thread'),
    url(r'^db/api/thread/remove/$', 'work_with_DB.api.thread.remove', name='remove_thread'),
    url(r'^db/api/thread/restore/$', 'work_with_DB.api.thread.restore', name='restore_thread'),
    url(r'^db/api/thread/listPosts/$', 'work_with_DB.api.thread.list_posts', name='list_posts_thread'),

)
