"""Helper functions."""


def get_following_users(connection, logname):
    """Get following users from databse."""
    cur = connection.execute(
        "SELECT username2 FROM following WHERE username1 = ?",
        (logname,)
    )
    return [row['username2'] for row in cur.fetchall()]


def get_followers(connection, logname):
    """Get followers from databse."""
    cur = connection.execute(
        "SELECT username1 FROM following WHERE username2 = ?",
        (logname,)
    )
    return [row['username1'] for row in cur.fetchall()]


def get_posts(connection, user):
    """Get posts from database."""
    cur = connection.execute(
        "SELECT postid, filename, owner, created "
        "FROM posts "
        "WHERE owner = ? ",
        (user,)
    )
    return cur.fetchall()


def get_owner_image_url(connection, owner):
    """Get owner profile picture."""
    cur = connection.execute(
        "SELECT filename AS owner_img_url "
        "FROM users "
        "WHERE username = ?",
        (owner,)
    )
    owner_filename = cur.fetchone()['owner_img_url']
    return f"/uploads/{owner_filename}"


def get_post_comments(connection, postid):
    """Get post comment from database."""
    cur = connection.execute(
        "SELECT owner, text "
        "FROM comments "
        "WHERE postid = ?",
        (postid,)
    )
    return [{"owner": row['owner'],
             "text": row['text']} for row in cur.fetchall()
            ]


def get_likes_count(connection, postid):
    """Get post like count."""
    cur = connection.execute(
        "SELECT COUNT(*) as likes "
        "FROM likes "
        "WHERE postid = ?",
        (postid,)
    )
    return cur.fetchone()['likes']


def get_full_name(connection, user_url_slug):
    """Get user fullname."""
    cur = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username == ?",
        (user_url_slug,)
    )
    return cur.fetchall()


def exist_dbase(connection, user_url_slug):
    """Check if a username exsit in database."""
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ?",
        (user_url_slug,)
    )
    return cur.fetchall()


def get_post_with_id(connection, postid_url_slug):
    """Get post with postid."""
    cur = connection.execute(
        "SELECT postid, filename AS img_url, owner, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid_url_slug,)
    )
    return cur.fetchone()


def liked_post(connection, postid_url_slug):
    """Check if a post is liked."""
    cur = connection.execute(
        "SELECT postid, owner "
        "FROM likes "
        "WHERE postid = ?",
        (postid_url_slug,)
    )
    return cur.fetchone()


def get_users(connection, logname):
    """Get users."""
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username != ?",
        (logname,)
    )
    return [row['username'] for row in cur.fetchall()]


def get_stored_password_from_db(connection, username):
    """Get password from database."""
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username=?",
        (username,)
    )
    return cur.fetchone()


# Given logname and postid, return likeid
def get_likeid(connection, logname, postid_url_slug):
    """Get post likeid."""
    cur = connection.execute(
        "SELECT likeid, owner, postid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (logname, postid_url_slug,)
    )
    return cur.fetchone()


# Given commontid, return owner
def get_comment_owner(connection, commentid):
    """Get comment owner."""
    cur = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )
    return cur.fetchone()


# Given postid, return owner
def get_post_owner(connection, postid):
    """Given postif, return owner."""
    cur = connection.execute(
        "SELECT owner "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )
    return cur.fetchone()


# Given postid, return filename
def get_post_filename(connection, postid):
    """Get filename."""
    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )
    return cur.fetchone()


# Given user1 and user2, return if followed
def check_follow(connection, username1, username2):
    """Get if followed."""
    cur = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (username1, username2)
    )
    return cur.fetchone()
