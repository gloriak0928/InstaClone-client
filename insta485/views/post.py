"""URLs include: /posts/."""
import pathlib
import uuid
import os
import flask
import insta485
from insta485.views.module import get_post_with_id
from insta485.views.module import get_post_comments
from insta485.views.module import get_likeid
from insta485.views.module import get_likes_count
from insta485.views.module import get_owner_image_url
from insta485.views.module import liked_post
from insta485.views.module import get_comment_owner
from insta485.views.module import get_post_owner
from insta485.views.module import get_post_filename
from insta485.views.module import check_follow


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Page for current post."""
    connection = insta485.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    post = get_post_with_id(connection, postid_url_slug)

    liked = liked_post(connection, postid_url_slug)
    context = {
        "logname": logname,
        "postid": postid_url_slug,
        "owner": post['owner'],
        "owner_img_url": get_owner_image_url(connection, post['owner']),
        "img_url": post['img_url'],
        "timetamp": post['created'],
        "likes": get_likes_count(connection, postid_url_slug),
        "comments": get_post_comments(connection, postid_url_slug),
        "is_liked": logname in liked['owner'] if liked is not None else False,
        "request_url": flask.request.path
    }

    return flask.render_template("post.html", **context)


@insta485.app.route('/likes/', methods=['POST'])
def post_like():
    """Request for likes."""
    connection = insta485.model.get_db()
    logname = flask.session['username']
    postid = flask.request.values.get('postid')
    likeid = get_likeid(connection, logname, postid)
    operation = flask.request.values.get('operation')
    if operation == "like":
        if likeid:
            flask.abort(409)
        else:
            connection.execute(
                "INSERT INTO likes "
                "(owner, postid) VALUES (?, ?)",
                (logname, postid, )
            )
    elif operation == "unlike":
        if not likeid:
            flask.abort(409)
        else:
            connection.execute(
                "DELETE "
                "FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname, postid, )
            )
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect("/")
    return flask.redirect(target)


@insta485.app.route('/comments/', methods=['POST'])
def post_comment():
    """Request for comments."""
    connection = insta485.model.get_db()
    logname = flask.session['username']
    operation = flask.request.values.get('operation')

    if operation == "create":
        postid = flask.request.values.get('postid')
        # Reuse operation to import text
        operation = flask.request.values.get('text')
        if not operation:
            flask.abort(400)
        else:
            connection.execute(
                "INSERT INTO comments"
                "(owner, postid, text) VALUES (?, ?, ?)",
                (logname, postid, operation)
            )
    elif operation == "delete":
        commentid = flask.request.values.get('commentid')
        comment_owner = get_comment_owner(connection, commentid)['owner']
        if comment_owner != logname:
            flask.abort(403)
        else:
            connection.execute(
                "DELETE "
                "FROM comments "
                "WHERE commentid = ?",
                (commentid, )
            )
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect("/")
    return flask.redirect(target)


@insta485.app.route('/posts/', methods=['POST'])
def post_post():
    """Request for posts."""
    operation = flask.request.values.get('operation')
    logname = flask.session['username']
    if operation == "create":
        post_post_create(logname)
    elif operation == "delete":
        post_post_delete(logname)
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect(f"/users/{logname}/")
    return flask.redirect(target)


# Helper function for post_post
def post_post_create(logname):
    """Request for creation of post."""
    connection = insta485.model.get_db()
    fileobj = flask.request.files['file']
    filename = fileobj.filename
    if not fileobj:
        flask.abort(400)
    else:
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection.execute(
                "INSERT INTO posts"
                "(filename, owner) VALUES (?, ?)",
                (uuid_basename, logname)
            )


# Helper function for post_post
def post_post_delete(logname):
    """Request for deletion of post."""
    connection = insta485.model.get_db()
    postid = flask.request.values.get('postid')
    post_owner = get_post_owner(connection, postid)['owner']
    if logname != post_owner:
        flask.abort(403)
    else:
        filename = get_post_filename(connection, postid)['filename']
        filename = pathlib.Path(filename)
        path = insta485.app.config["UPLOAD_FOLDER"]/filename
        os.remove(path)
        connection.execute(
                "DELETE "
                "FROM posts "
                "WHERE postid = ?",
                (postid, )
            )


@insta485.app.route('/following/', methods=['POST'])
def post_following():
    """Request for following or follower."""
    connection = insta485.model.get_db()
    logname = flask.session['username']
    operation = flask.request.values.get('operation')
    username2 = flask.request.values.get('username')
    check = check_follow(connection, logname, username2)
    # user1 follows user2
    if operation == "unfollow":
        if not check:
            flask.abort(409)
        else:
            connection.execute(
                "DELETE "
                "FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (logname, username2)
            )
    elif operation == "follow":
        if check_follow(connection, logname, username2):
            flask.abort(409)
        else:
            connection.execute(
                "INSERT INTO following "
                "(username1, username2) VALUES (?, ?)",
                (logname, username2)
            )
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect("/")
    return flask.redirect(target)
