from app import app, db, login_manager
from flask import request, render_template, flash, redirect, url_for, session
from models import *
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
from forms import *
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
def home():
    signin_form = SignInForm()

    if signin_form.validate_on_submit():
        username = signin_form.username.data
        user_object = User.get(username)
        if user_object and user_object.check_password(signin_form.password.data):
            login_user(user_object)
            flash("Successfully logged in")
            return redirect(f'/{username}')
        elif not user_object:
            flash(f'There is no user with this username: {username}')
            return redirect("/")
        else:
            flash('Incorrect password')

    return render_template('home.html', sform=signin_form)


@app.route('/signup', methods=['GET', 'POST'])
def signuppage():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        if User.get(username) is None:
            user_object = User(username=username, password_hash=None)
            user_object.set_password(signup_form.password.data)
            db.session.add(user_object)
            db.session.commit()
            flash("Successfully signed up")
            return redirect("/")
        else:
            flash("That username already exists. Please choose another.")

    return render_template('signup.html', form=signup_form)


@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def userpage(username):
    user = User.get(username)
    current_protests = Protest.getPagination()

    return render_template('user.html', user=user, protests=current_protests)


@app.route('/<username>/create_protest', methods=['GET', 'POST'])
@login_required
def create_new_protest(username):
    user = User.get(username)
    make_new_protest = OrganizeProtest()

    if make_new_protest.validate_on_submit():
        title = make_new_protest.title.data
        description = make_new_protest.description.data
        location = make_new_protest.location.data
        date = make_new_protest.date.data
        new_protest_object = Protest(title=title, description=description, location=location, date=date)
        user.created_protests.append(new_protest_object)
        new_protest_object.addAttendee(username)
        db.session.add(new_protest_object)
        db.session.commit()
        flash("Successfully Created a Protest")
        return redirect(f'/{username}')

    return render_template('make_protest.html', form=make_new_protest)


@app.route('/<username>/<protest>', methods=['GET', 'POST'])
@login_required
def protest(username, protest):
    user = User.get(username)
    curr_protest = Protest.get(protest)

    return render_template('user.html', user=user, protests=curr_protest)


@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect('/')


@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized')
    return redirect("/")