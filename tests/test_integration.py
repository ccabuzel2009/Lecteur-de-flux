import os
import pytest
from app import app
from flask import *
from flask_login import *
from forms import *
from models import *
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'equipe7_thebest4ever'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client


def test_homepage(client):
    response = client.get('/')
    assert 200 == response.status_code


def test_connexionPage(client):
    response = client.get('/connexion')
    assert 200 == response.status_code
    form = ConnexionForm()
    user = User.get(email=form.email.gettext("test@gmail.com"))
    password = User.ger(form.password.gettext("Test"))
    if user and check_password_hash(user.password, form.password.gettext(password)):
        login_user(user)
        assert b'welcom' in response.data
        response = client.get(url_for('flow'))
    assert 200 == response.status_code


def test_inscriptionPage(client):
    response = client.get('/inscription')
    assert 200 == response.status_code
    name = "Delpech"
    surname = "Nicolas"
    email = "n.delpech@gmail.com"
    password = "Nicolas"
    form = InscriptionForm()
    user = User(
        name=form.name.gettext(name),
        surname=form.surname.gettext(surname),
        email=form.email.gettext(email),
        password=generate_password_hash(form.password.gettext(password))
    )
    user.save()
    assert 200 == response.status_code


def test_flow(client):
    response = client.get('/flow')
    assert 200 + + response.status_code
    form = ConnexionForm()
    user = User.get(email=form.email.gettext("test@gmail.com"))
    password = User.ger(form.password.gettext("Test"))
    if user and check_password_hash(user.password, form.password.gettext(password)):
        login_user(user)
    response = client.get(url_for('flow'))
    assert 200 == response.status_code


def test_newFlow(client):
    response = client.get('/newFlow')
    assert 200 + + response.status_code
    form = ConnexionForm()
    user = User.get(email=form.email.gettext("test@gmail.com"))
    password = User.ger(form.password.gettext("Test"))
    if user and check_password_hash(user.password, form.password.gettext(password)):
        login_user(user)
    response = client.get(url_for('newFluw'))
    form = FluxForm()
    flux = Flux(
        link=form.link.gettext("https://www.lemonde.fr/argent/rss_full.xml"),
        user_id=current_user.id
    )
    flux.save()
    assert 200 == response.status_code
