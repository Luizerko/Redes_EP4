import os
from flask import Flask, render_template, url_for, request, flash, redirect, abort
import webbrowser
from flask_login import login_user
from wtforms import Form, StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
#from flask_security import Security, SQLAlchemyUserDatastore, auth_required
#from flask_security.models import fsqla_v2 as fsqla

site = Flask(__name__)
site.config['DEBUG'] = True
site.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
site.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
site.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

# db = SQLAlchemy(site)
# fsqla.FsModels.Set_db_info(db)

# class Role(db.Model, fsqla.FsRoleMixin):
#     pass

# class User(db.Model, fsqla.FsUserMixin):
#     pass

class LoginForm(Form):
    username = StringField('usuario')
    password = PasswordField('senha')

form = LoginForm()

#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(site, user_datastore)

# @site.before_first_request
# def create_test_user():
#     db.create_all()
#     if not user_datastore.find_user(usuario="patrick"):
#         user_datastore.create_user(usuario="patrick", senha="lui")
#     db.session.commit()

@site.route('/', methods=['GET', 'POST'])
@site.route('/login', methods=['GET', 'POST'])
def login():
    #user = SQLAlchemyUserDatastore(db, User, Role)
    #user.find_user(usuario=form.data['usuario'])
    global form
    print(request.data)
    if request.method == 'POST':
        
        usuario = form.username.data
        senha = form.password.data

        print(usuario)
        print(senha)

        if usuario == 'patrick' and senha == 'lui':
            flash('Você logou com sucesso!')
            return redirect(url_for('/logado'))

        flash('Falha ao logar!')
    return render_template('login.html', form=form)

@site.route('/logado', methods=['GET', 'POST'])
def logado():
    return render_template('logado.html')

if __name__ == '__main__':
    site.run(debug=True)