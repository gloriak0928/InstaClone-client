"""URLs include: '/users/<user_url_slug>/followers/'."""

import flask
import insta485
from insta485.views.module import get_followers
from insta485.views.module import get_owner_image_url
from insta485.views.module import get_following_users
from insta485.views.module import exist_dbase


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_follower(user_url_slug):
    """Display /users/<user_url_slug>/followers/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    if not exist_dbase(connection, user_url_slug):
        flask.abort(404)

    follower_names = get_followers(connection, user_url_slug)
    followers = []

    logname_following = get_following_users(connection, logname)
    logname_following.append(logname)

    for name in follower_names:
        follower = {
            "username": name,
            "user_img_url": get_owner_image_url(connection, name),
            "logname_follows_username": name in logname_following
        }
        followers.append(follower)

    context = {
        "logname": logname,
        "followers": followers,
        "request_url": flask.request.path
    }

    return flask.render_template("followers.html", **context)
