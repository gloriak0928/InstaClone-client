"""Views, one for each Insta485 page."""
# from module.py import function
from insta485.views.index import show_index
from insta485.views.user import show_users
from insta485.views.follower import show_follower
from insta485.views.following import show_following
from insta485.views.post import show_post
from insta485.views.post import post_like
from insta485.views.post import post_comment
from insta485.views.post import post_post
from insta485.views.post import post_post_create
from insta485.views.post import post_post_delete
from insta485.views.post import post_following
from insta485.views.explore import show_explore
from insta485.views.account import show_account_login
from insta485.views.account import show_account_logout
from insta485.views.account import show_account_create
from insta485.views.account import show_account_delete
from insta485.views.account import show_account_edit
from insta485.views.account import show_account_password
from insta485.views.account import account_post_request
from insta485.views.account import account_auth
