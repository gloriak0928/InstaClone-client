"""URLs include: '/users/<user_url_slug>/following/'."""

import flask
import insta485
from insta485.views.module import get_following_users, get_owner_image_url
from insta485.views.module import exist_dbase


@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Display /users/<user_url_slug>/following/ route."""
    connection = insta485.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    if not exist_dbase(connection, user_url_slug):
        flask.abort(404)

    following_names = get_following_users(connection, user_url_slug)
    following = []

    logname_following = get_following_users(connection, logname)
    logname_following.append(logname)

    for name in following_names:
        people = {
            "username": name,
            "user_img_url": get_owner_image_url(connection, name),
            "logname_follows_username": name in logname_following
        }
        following.append(people)

    context = {
        "logname": logname,
        "following": following,
        "request_url": flask.request.path
    }

    return flask.render_template("following.html", **context)
