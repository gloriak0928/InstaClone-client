"""REST API for likes."""
import flask
import insta485
from insta485.views.module import check_auth
from insta485.views.module import get_likeid
from insta485.views.module import get_post_with_id
from insta485.views.module import get_like_details_by_likeid


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/likes/?postid=<postid>', methods=['POST'])
def post_like_api(postid):
    """Create a new like for the specified post id."""
    connection = insta485.model.get_db()
    username = check_auth(connection)
    likeid = get_likeid(connection, username, postid)
    post = get_post_with_id(connection, postid)
    if not post:
        flask.abort(404)

    # FIXME: 404 page not found
    message_code = 200
    if not likeid:
        connection.execute(
            "INSERT INTO likes (owner, postid) "
            "VALUES (?, ?)",
            (username, postid,)
        )
        likeid = get_likeid(connection, username, postid)
        message_code = 201

    context = {
        "likeid": likeid['likeid'],
        "url": f"/api/v1/likes/{likeid['likeid']}/"
    }
    return flask.jsonify(**context), message_code


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete the like based on the like id."""
    connection = insta485.model.get_db()
    username = check_auth(connection)
    like = get_like_details_by_likeid(connection, likeid)
    if not like:
        flask.abort(404)
    elif like['owner'] != username:
        flask.abort(403)
    connection.execute(
        "DELETE FROM likes WHERE likeid = ?", (likeid,)
    )
    return flask.jsonify(), 204