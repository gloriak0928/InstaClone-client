"""REST API for posts."""
import flask
import insta485
from insta485.views.module import check_auth
from insta485.views.module import get_post_with_id
from insta485.views.module import get_likeid
from insta485.views.module import get_likes_count
from insta485.views.module import get_comment_details_by_postid
from insta485.views.module import get_owner_image_url


# Every REST API route should return 403
# if a user is not authenticated.
# The only exception is /api/v1/, which is publicly available.

# @insta485.app.route('/api/v1/posts/<postid>/')
# def get_one_post():
#     """Return one post, including comments and likes."""

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post_details_api(postid_url_slug):
    """Return N newest post urls and ids."""
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
        "lognameLikesThis": bool(comments),
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
        "ownerImgUrl": f"{get_owner_image_url(connection, username)}",
        "ownerShowUrl": f"/users/{username}/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
        }
    return flask.jsonify(**context)


# @insta485.app.route('/api/v1/posts/?size=N')
# def get_N_posts():


@insta485.app.route('/api/v1/posts/')
def get_n_posts_api():
    """Return 10 newest post urls and ids."""
    connection = insta485.model.get_db()

    # Check if authorized
    username = check_auth(connection)

    # Retrieve data
    postid_lte = flask.request.args.get('postid_lte')
    size = flask.request.args.get('size', default=10, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    if size <= 0 or page < 0:
        flask.abort(400)
    offset = 0
    next_url = ""
    if page != 0:
        offset = size*page
    # return str(postid_lte)
    # connection.execute("PRAGMA foreign_keys = ON")
    # connection.execute("DELETE FROM likes")
    # connection.execute("DELETE FROM comments")
    # connection.execute("DELETE FROM posts")

    # Create exactly 11 posts
    # for _ in range(11):
    #     connection.execute(
    #         "INSERT INTO posts(owner, filename) "
    #         "VALUES('awdeorio', 'fox.jpg') ",
    #     )

    if not postid_lte:
        postid_lte = connection.execute(
            "SELECT postid FROM posts ORDER BY postid DESC"
        ).fetchone()['postid']
    posts = connection.execute(
        "SELECT postid FROM posts "
        "WHERE postid <= ? AND "
        "(owner IN (SELECT username2 FROM following WHERE username1 = ?) OR "
        "owner = ?) "
        "ORDER BY postid DESC LIMIT ? OFFSET ?",
        (postid_lte, username, username, size, offset,)
        ).fetchall()

    if size <= len(posts):
        next_url = (
            f"/api/v1/posts/?size={size}&"
            f"page={page+1}&"
            f"postid_lte={postid_lte}"
        )
    for post in posts:
        post["url"] = f"/api/v1/posts/{post['postid']}/"
    context = {"next": next_url,
               "results": posts,
               "url": flask.url_for('get_n_posts_api', **flask.request.args)
               }
    return flask.jsonify(**context)
