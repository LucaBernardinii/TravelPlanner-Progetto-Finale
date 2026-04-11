from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Utente
from app.repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']

        repo = UserRepository()
        if repo.get_by_email(email):
            flash('Email gia registrata.')
            return redirect(url_for('auth.register'))

        utente = Utente(nome, email, generate_password_hash(password))
        repo.create(utente)
        flash('Registrazione completata. Accedi.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        repo = UserRepository()
        utente = repo.get_by_email(email)

        if utente and check_password_hash(utente.password_hash, password):
            session['utente_id'] = utente.id
            session['utente_nome'] = utente.nome
            return redirect(url_for('trips.index'))

        flash('Credenziali non valide.')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
