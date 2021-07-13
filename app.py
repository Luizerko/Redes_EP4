from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, \
    UserMixin, RoleMixin
from flask_security.utils import hash_password
from flask_cors import CORS
from flask import session
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5001"], supports_credentials=True)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECURITY_PASSWORD_SALT'] = 'thisisasecretsalt'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/profile'
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['SECURITY_BACKWARDS_COMPAT_AUTH_TOKEN'] = True
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role', 
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_datastore.create_user(
            email=request.form.get('email'),
            password=hash_password(request.form.get('password'))
        )
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('register.html')

# @app.route('/logln', methods=['POST', 'GET'])
# def logln():
#     return render_template('logln.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.after_request
def cookies(response):
    same_cookie = session_cookie.dumps(dict(session))
    response.headers.add("Set-Cookie", f"session={same_cookie}; Secure; SameSite=None; Path=/;")
    return response

if __name__ == '__main__':
    app.run(debug=True)