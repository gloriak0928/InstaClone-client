"""Insta485 REST API."""

from insta485.api.index import get_index_api
from insta485.api.posts import get_post_details_api
from insta485.api.posts import get_N_posts_api
from insta485.api.likes import post_like_api
from insta485.api.likes import delete_like_api
from insta485.api.comments import post_comment_api
# from insta485.api.comments import delete_comment