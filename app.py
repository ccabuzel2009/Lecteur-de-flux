import sqlite3
import click
import feedparser

from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from models import *

app = Flask(__name__)
app.secret_key = 'Antoine'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET', 'POST', ])
def home():
    form = InscriptionForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        user.save()
    return render_template("index.html", form=form)


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = ConnexionForm()
    if form.validate_on_submit():
        user = User.get(email=form.email.data)
        user.is_active = True
        User.is_authenticated = True
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Welcome')
            if user.is_authenticated:
                return redirect(url_for('flux'))
    return render_template("connexion.html", form=form)


@login_required
@app.route('/deconnexion')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/flux', methods=['GET', 'POST'])
@login_required
def flux():
    connexion = sqlite3.connect("flux.sqlite3")
    curseur = connexion.cursor()
    my_user = current_user.get_id()

    curseur.execute("""SELECT link FROM flux WHERE user_id=?""", (my_user,))
    resultats = curseur.fetchall()

    root = []
    for url in resultats:
        url = url[0]
        root.append(feedparser.parse(url))

    return render_template("flux.html", root=root)


@app.route('/newflux', methods=['GET', 'POST'])
@login_required
def newflux():
    form = FluxForm()
    if form.validate_on_submit():
        flux = Flux(
            link=form.link.data,
            user_id=current_user.id
        )
        flux.save()
    return render_template("newflux.html", form=form)


@app.cli.command()
def initdb():
    create_tables()
    click.echo('Initialized the database')


@app.cli.command()
def dropdb():
    drop_tables()
    click.echo('Dropped tables from database')
