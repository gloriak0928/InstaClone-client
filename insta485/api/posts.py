"""REST API for posts."""
import flask
import insta485


# Every REST API route should return 403 
# if a user is not authenticated. 
# The only exception is /api/v1/, which is publicly available.
@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.

    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "postid": 1,
      "url": "/api/v1/posts/1/"
    }
    """
    # FIXME: 不知道这部分是干嘛的
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/?size=10')
def get_ten_posts():
    """Return 10 newest post urls and ids."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/posts/?size=N')
def get_N_posts():
    """Return N newest post urls and ids."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/posts/?page=N')
def get_N_pages():
    """Return N’th page of post urls and ids."""
    # TODO: Need to finish


@insta485.app.route('/api/v1/posts/?postid_lte=N')
def get_old_posts():
    """Return post urls and ids no newer than post id N."""
    # TODO: Need to finish

  
@insta485.app.route('/api/v1/posts/<postid>/')
def get_one_post():
    """Return one post, including comments and likes."""
    # TODO: Need to finish
