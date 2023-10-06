"""REST API for comments."""
import flask
import insta485


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/comments/?postid=<postid>')
def post_comment():
    """Create a new comment based on the text 
    in the JSON body for the specified post id."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/comments/<commentid>/')
def delete_comment():
    """Delete the comment based on the comment id."""
    # TODO: Need to finish