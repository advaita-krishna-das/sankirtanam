from flask import Flask, request, redirect, abort, Response
from flask_login import LoginManager, UserMixin, login_user

from app.admin.admin import admin
from app.admin.documents import documents
from app.admin.reports import reports as admin_reports
from app.autocomplete import autocomplete
from app.reception import reception
from app.reports import reports

app = Flask(__name__)
app.secret_key = "SOME-SECRET-GOES-HERE-HARE-KRISHNA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Our mock database.
users = {'admin@sankirtanam.ru': {'password': 'secret'}}


class User(UserMixin):
    def __init__(self, login):
        self.__login = login

    def get_id(self):
        return self.__login


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User(email)
    user.id = email
    return user


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


app.register_blueprint(reception, url_prefix="/reception")
app.register_blueprint(autocomplete, url_prefix="/autocomplete")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(documents, url_prefix="/admin/documents")
app.register_blueprint(admin_reports, url_prefix="/admin/reports")
app.register_blueprint(reports, url_prefix="/reports")

