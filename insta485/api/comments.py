"""REST API for comments."""
import flask
import insta485
import sqlite3
from insta485.views.module import check_auth
from insta485.views.module import get_post_with_id



# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/comments/', methods=['POST'])
def post_comment_api():
    """Create a new comment based on the text 
    in the JSON body for the specified post id."""
    # TODO: Need to finish
    connection = insta485.model.get_db()
    username = check_auth(connection)
    postid = flask.request.args.get('postid')
    text = flask.request.json['text']
    post = get_post_with_id(connection, postid)
    if not post:
        flask.abort(404)
    connection.execute(
        "INSERT INTO comments"
        "(owner, postid, text) VALUES (?, ?, ?)",
        (username, postid, text)
    )
    new_comment = connection.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()["last_insert_rowid()"]
    context = {
        "commentid": new_comment,
        "lognameOwnsThis": True,
        "owner": username,
        "ownerShowUrl": f"/users/{username}/",
        "text": text,
        "url": f"/api/v1/comments/{new_comment}/"
    }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment_api():
    """Delete the comment based on the comment id."""
    # TODO: Need to finish