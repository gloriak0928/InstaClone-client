"""REST API for posts."""
import hashlib
import flask
import arrow
import insta485
from insta485.views.module import check_auth
from insta485.views.module import get_post_with_id
from insta485.views.module import get_post_only_id
from insta485.views.module import liked_post, get_likeid
from insta485.views.module import get_post_comments, get_likes_count
from insta485.views.module import get_comment_details_by_postid


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.

@insta485.app.route('/api/v1/posts/<postid>/')
def get_one_post():
    """Return one post, including comments and likes."""
    # TODO: Need to finish

#这两个好像是同一个东西

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post_details(postid_url_slug):
    """Return one post, including comments and likes.

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
    connection = insta485.model.get_db()
    username = check_auth(connection)
    post = get_post_with_id(connection, postid_url_slug)
    if not post:
        flask.abort(404)
    comment_list = []
    comments = get_comment_details_by_postid(connection, postid_url_slug)
    for comment in comments:
        comment_list.append({
            "commentid": comment['commentid'],
            "lognameOwnsThis": (username == comment['owner']),
            "owner": comment['owner'],
            "ownerShowUrl": f"/users/{comment['owner']}/",
            "text": comment['text'],
            "url": f"/api/v1/comments/{comment['commentid']}/"
        })
    comments = get_likeid(connection, username, postid_url_slug)
    likes = {
        "lognameLikesThis": (comments != None),
        "numLikes": get_likes_count(connection, postid_url_slug),
        "url": None
        }
    if likes["lognameLikesThis"]:
        likes["url"] = f"/api/v1/likes/{comments['likeid']}/"
    
    # Interegate information
    context = {
        "comments": comment_list,
        "comments_url": f"/api/v1/comments/?postid={postid_url_slug}",
        "created": post['created'],
        "imgUrl": f"/uploads/{post['img_url']}",
        "likes": likes,
        "owner": username,
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": f"/users/{username}/",
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

