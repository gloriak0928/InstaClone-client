"""URLs include: '/explore/'."""

import flask
import insta485
from insta485.views.module import get_following_users
from insta485.views.module import get_users
from insta485.views.module import get_owner_image_url


@insta485.app.route('/explore/')
def show_explore():
    """Display /exlore/ route."""
    connection = insta485.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    following = get_following_users(connection, logname)
    all_users = get_users(connection, logname)
    not_following = []

    for user in all_users:
        if user not in following:
            user_info = {
                "username": user,
                "user_img_url": get_owner_image_url(connection, user)
            }
            not_following.append(user_info)

    context = {"logname": logname,
               "not_following": not_following,
               "request_url": flask.request.path
               }

    return flask.render_template("explore.html", **context)
