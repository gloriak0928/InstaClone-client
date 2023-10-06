"""REST API for likes."""
import flask
import insta485


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/likes/?postid=<postid>')
def post_like():
    """Create a new like for the specified post id."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/likes/<likeid>/')
def delete_like():
    """Delete the like based on the like id."""
    # TODO: Need to finish
