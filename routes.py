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
            return redirect(f'/{username}/news')
        elif not user_object:
            flash(f'There is no user with this username: {username}')
            return redirect("/")
        else:
            flash('Incorrect password')

    return render_template('login.html', sform=signin_form)


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

    return render_template('register.html', sform=signup_form)


@app.route('/<username>/news', methods=['GET', 'POST'])
@login_required
def userpage_news(username):
    user = User.get(username)
    current_news = News.getPagination()
    return render_template('news.html', user=user, news_list=current_news)


@app.route('/<username>/protests', methods=['GET', 'POST'])
@login_required
def userpage_protests(username):
    user = User.get(username)
    current_protests = Protest.getPagination()
    return render_template('protests.html', user=user, protests_list=current_protests)


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

    return render_template('new_protest.html', form=make_new_protest)

@app.route('/<username>/update_my_protest/<id>', methods=['GET', 'POST'])
@login_required
def update_existing_protest(username, id):
    user = User.get(username)
    update_protest = UpdateProtest()

    if update_protest.validate_on_submit():
        title = update_protest.title.data
        description = update_protest.description.data
        location = update_protest.location.data
        date = update_protest.date.data
        new_protest_object = Protest(title=title, description=description, location=location, date=date)
        user.created_protests.append(new_protest_object)
        new_protest_object.addAttendee(username)
        db.session.add(new_protest_object)
        db.session.commit()
        flash("Successfully Created a Protest")
        return redirect(f'/{username}')

    return render_template('new_protest.html', form=update_protest)


@app.route('/<username>/<protest>', methods=['GET', 'POST'])
@login_required
def protest(username, protest_):
    user = User.get(username)
    curr_protest = Protest.get(protest_)

    return render_template('view_protest.html', user=user, protest=curr_protest)


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