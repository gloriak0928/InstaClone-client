"""Flask routes for Insta485 user account operations."""
import hashlib
import pathlib
import uuid
import os
import flask
import insta485
from insta485.views.module import get_stored_password_from_db
from insta485.views.module import exist_dbase
from insta485.views.module import get_owner_image_url


@insta485.app.route('/uploads/<filename>')
def static_file_permission(filename):
    """For static file upload."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        filepath = insta485.app.config['UPLOAD_FOLDER']/filename
        if not os.path.exists(filepath):
            flask.abort(404)
        return flask.send_from_directory(
            insta485.app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )


@insta485.app.route('/accounts/auth/')
def account_auth():
    # 检查用户是否login
    """For AWS Deploy."""
    if 'username' not in flask.session:
        flask.abort(403)
    return ('', 200)


@insta485.app.route('/accounts/login/')
def show_account_login():
    """Page for account login."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("account.html")


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_account_logout():
    """Page for account logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_account_login'))


@insta485.app.route('/accounts/create/')
def show_account_create():
    """Page for create an account."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_account_edit'))
    return flask.render_template("create.html")


@insta485.app.route('/accounts/delete/')
def show_account_delete():
    """Page for create an account."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))
    logname = flask.session['username']
    context = {
        "logname": logname,
    }
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/')
def show_account_edit():
    """Page for edit an account."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    connection = insta485.model.get_db()
    logname = flask.session['username']

    cur = connection.execute(
        "SELECT fullname, email, filename "
        "FROM users "
        "WHERE username = ?",
        (logname, )
    )
    user = cur.fetchone()

    context = {
        "logname": logname,
        "fullname": user['fullname'],
        "email": user['email'],
        "filename": user['filename'],
        "request_url": flask.request.path
    }
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/')
def show_account_password():
    """Page for changing password."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))
    logname = flask.session['username']
    context = {'logname': logname}
    return flask.render_template("password.html", **context)


@insta485.app.route('/accounts/', methods=['POST'])
def account_post_request():
    """Operation for /accounts/?=target=URL."""
    operation = flask.request.values.get('operation')
    if operation == "login":
        login()
    elif operation == "create":
        create()
    elif operation == "delete":
        delete()
    elif operation == "edit_account":
        edit()
    elif operation == "update_password":
        update_password()
    target = flask.request.args.get('target')
    if target:
        return flask.redirect(target)
    return flask.redirect(flask.url_for('show_index'))


def login():
    """Request for handling operation login."""
    connection = insta485.model.get_db()

    username = flask.request.form['username']
    password = flask.request.form['password']

    if not username or not password:
        flask.abort(400)

    stored_password = get_stored_password_from_db(connection, username)

    if stored_password is None:
        flask.abort(403)

    hashed_password = stored_password['password']
    salt = hashed_password.split('$')[1]

    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    if password_db_string != hashed_password:
        flask.abort(403)

    flask.session['username'] = username


def create():
    """Request for handling operation create."""
    connection = insta485.model.get_db()

    username = flask.request.form['username']
    password = flask.request.form['password']
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    pic = flask.request.files["file"]

    if not username or not password or not fullname or not email or not pic:
        flask.abort(400)

    if len(exist_dbase(connection, username)) != 0:
        flask.abort(409)

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    hash_obj = "$".join([algorithm, salt, password_hash])

    filename = pic.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    pic.save(insta485.app.config["UPLOAD_FOLDER"]/uuid_basename)

    connection.execute(
        "INSERT INTO users(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?) ",
        (username, fullname, email, uuid_basename, hash_obj)
    )

    flask.session['username'] = username


def delete():
    """Request for handling operation create."""
    if 'username' not in flask.session:
        flask.abort(403)

    connection = insta485.model.get_db()
    # remove profile images
    filename = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",
        (flask.session['username'],)
    ).fetchone()
    if filename:
        path = insta485.app.config['UPLOAD_FOLDER']/filename['filename']
        os.remove(path)

    # remove post images
    filename = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ?",
        (flask.session['username'],)
    ).fetchall()
    if filename:
        for file in filename:
            path = insta485.app.config['UPLOAD_FOLDER']/file['filename']
            os.remove(path)

    connection.execute(
        "DELETE "
        "FROM Users "
        "WHERE username = ?",
        (flask.session['username'],)
    )

    flask.session.clear()


def edit():
    """Request for handling operation edit."""
    connection = insta485.model.get_db()

    if 'username' not in flask.session:
        flask.abort(403)

    logname = flask.session['username']

    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    pic = flask.request.files.get('file')

    if not fullname or not email:
        flask.abort(400)

    if pic is None:
        connection.execute(
            "UPDATE users SET fullname=?, "
            "email=? WHERE username=?",
            (fullname, email, logname)
        )
    else:
        filename = pic.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        pic.save(path)
        old_photo = get_owner_image_url(connection, logname)
        if os.path.exists(insta485.app.config["UPLOAD_FOLDER"] / old_photo):
            os.remove(insta485.app.config["UPLOAD_FOLDER"] / old_photo)

        connection.execute(
            "UPDATE users "
            "SET fullname=?, email=?, filename=? WHERE username=?",
            (fullname, email, uuid_basename, logname)
        )


def update_password():
    """Request for handling operation update password."""
    if 'username' not in flask.session:
        flask.abort(403)

    connection = insta485.model.get_db()
    logname = flask.session['username']

    password = flask.request.form.get('password')
    new_password1 = flask.request.form.get('new_password1')
    new_password2 = flask.request.form.get('new_password2')

    if not password or not new_password1 or not new_password2:
        flask.abort(400)

    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (logname,)
    )
    stored_password = cur.fetchone()
    hashed_password = stored_password['password']
    salt = hashed_password.split('$')[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    hash_obj = "$".join([algorithm, salt, password_hash])

    if hash_obj != hashed_password:
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    new_password_salted = salt + new_password1
    hash_obj.update(new_password_salted.encode('utf-8'))
    new_password_hash = hash_obj.hexdigest()
    hash_obj = "$".join([algorithm, salt, new_password_hash])

    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username = ?",
        (hash_obj, logname)
    )
