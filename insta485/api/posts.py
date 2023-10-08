"""REST API for posts."""
import hashlib
import flask
import arrow
import insta485
from insta485.views.module import check_auth
from insta485.views.module import get_stored_password_from_db
from insta485.views.module import get_following_users, get_posts, get_post_only_id
from insta485.views.module import get_owner_image_url
from insta485.views.module import get_post_comments, get_likes_count


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.

@insta485.app.route('/api/v1/posts/<postid>/')
def get_one_post():
    """Return one post, including comments and likes."""
    # TODO: Need to finish

#这两个好像是同一个东西

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.

    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "postid": 1,
      "url": "/api/v1/posts/1/"
    }
    """
    # FIXME: 不知道这部分是干嘛的
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


# @insta485.app.route('/api/v1/posts/?size=N')
# def get_N_posts():
    """Return N newest post urls and ids."""
    # TODO: Need to finish

# 这两个好像也是一个东西

@insta485.app.route('/api/v1/posts/')
def get_N_posts():
    """Return 10 newest post urls and ids."""
    # TODO: Need to finish
    connection = insta485.model.get_db()
    
    # Check if authorized
    username = check_auth(connection)
    
    # Retrieve data
    postid_lte = flask.request.args.get('postid_lte', default=3, type=int)
    size = flask.request.args.get('size', default=10, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    if size <= 0 or page < 0:
        flask.abort(400)
    offset = 0
    next = ""
    if page != 0:
        offset = size*page
    if size < postid_lte:
        next = f"/api/v1/posts/?size={size}&page={page+1}&postid_lte={postid_lte}/"

    posts = get_post_only_id(connection, username, postid_lte, size, offset)

    for post in posts:
        post["url"] = f"/api/v1/posts/{post['postid']}"
    context = {"next": next,
               "results": posts,
               "url": flask.request.path
               }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/?page=N')
def get_N_pages():
    """Return N’th page of post urls and ids."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/posts/?postid_lte=N')
def get_old_posts():
    """Return post urls and ids no newer than post id N."""
    # TODO: Need to finish

