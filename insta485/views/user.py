"""URLs include: /users/<user_url_slug>."""

import flask
import insta485
from insta485.views.module import get_full_name
from insta485.views.module import get_followers
from insta485.views.module import get_following_users
# from insta485.views.module import get_posts
from insta485.views.module import exist_dbase


@insta485.app.route('/users/<user_url_slug>/')
def show_users(user_url_slug):
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    if len(exist_dbase(connection, user_url_slug)) == 0:
        flask.abort(404)

    following_users = get_following_users(connection, logname)
    following_users.append(logname)
    logname_follows_username = user_url_slug in following_users

    cur = connection.execute(
        "SELECT postid, filename AS img_url "
        "FROM posts "
        "WHERE owner = ?",
        (user_url_slug,)
    )
    posts = cur.fetchall()
    print("logname: ")
    print(logname)
    context = {
        "logname": logname,
        "username": user_url_slug,
        "logname_follows_username": logname_follows_username,
        "fullname": get_full_name(connection, user_url_slug),
        "following": len(get_following_users(connection, user_url_slug)),
        "followers": len(get_followers(connection, user_url_slug)),
        "total_posts": len(posts),
        "posts": posts,
        "request_url": flask.request.path
    }

    return flask.render_template("user.html", **context)
