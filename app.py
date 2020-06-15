"""Flask app for users/login"""

from flask import Flask, url_for, render_template, redirect, flash, jsonify, request, session

from models import db, connect_db, User, Feedback

from forms import RegistrationForm, LoginForm, FeedbackForm

from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SECRET_KEY'] = "ManchesterU"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


@app.route('/')
def get_homepage():
    """Redirect users to login page"""
    return redirect('/register')


@app.route('/logged-in', methods=["Get", "POST"])
def login():
    """Take user to logged in page"""
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect('/')
    form = FeedbackForm()
    all_feedback = Feedback.query.all()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(
            title=title, content=content, username=session['username'])
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback submited', 'primary')
        return redirect('/logged-in')
    return render_template('authenticated.html', form=form, feedback=all_feedback)


@app.route('/logged-in/<int:id>', methods=["POST"])
def delete_feedback(id):
    """Delete user feedback"""
    if 'username' not in session:
        flash('Please login to continue', 'danger')
        return redirect('/login')
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted!', 'info')
        return redirect('/logged-in')
    flash("You don't have permission to do that", 'danger')
    return redirect('/logged-in')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """render registration and login form"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('That username is not available')
            return render_template('registration.html', form=form)
        session['username'] = new_user.username
        flash("Welcome to your account", 'primary')
        return redirect('/logged-in')
    return render_template('registration.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}', 'primary')
            session['username'] = user.username
            return redirect('/logged-in')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage"""

    session.pop('username')
    flash("You have logged out", 'success')

    return redirect('/')
