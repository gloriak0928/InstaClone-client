"""REST API for index page."""
import flask
import insta485


# Every REST API route should return 403
# if a user is not authenticated.
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/')
def get_index_api():
    """Return API resource URLs."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)
