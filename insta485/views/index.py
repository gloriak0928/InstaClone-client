"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485
from insta485.views.module import get_following_users, get_posts
from insta485.views.module import get_owner_image_url
from insta485.views.module import get_post_comments, get_likes_count


@insta485.app.route('/')
def show_index():
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    logname = flask.session['username']

    following_users = get_following_users(connection, logname)
    following_users.append(logname)
    posts = []
    for user in following_users:
        posts.extend(get_posts(connection, user))

    for post in posts:
        post["owner_img_url"] = get_owner_image_url(connection, post['owner'])
        post["timestamp"] = arrow.get(post["created"]).humanize()
        post["likes"] = get_likes_count(connection, post['postid'])
        post["comments"] = get_post_comments(connection, post['postid'])

    context = {"posts": posts,
               "logname": logname,
               "request_url": flask.request.path
               }

    return flask.render_template("index.html", **context)
