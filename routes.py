from app import app, db, login_manager
from flask import request, render_template, flash, redirect, url_for, session
from models import *
from flask_login import current_user, login_user, logout_user, login_required
from forms import *


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == "POST":
        username = request.form['username']
        user_object = User.get(username)
        if user_object and user_object.check_password(request.form['password']):
            login_user(user_object)
            flash("Successfully logged in")
            return redirect(f'/{username}/news/{1}')
        elif not user_object:
            flash(f'There is no user with this username: {username}')
            return redirect("/")
        else:
            flash('Incorrect password')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signuppage():

    if request.method == "POST":
        username = request.form['username']
        if User.get(username) is None:
            user_object = User(username=username, password_hash=None)
            user_object.set_password(request.form['password'])
            db.session.add(user_object)
            db.session.commit()
            flash("Successfully signed up")
            return redirect("/")
        else:
            flash("That username already exists. Please choose another.")

    return render_template('register.html')


@app.route('/<username>/news/<i>', methods=['GET', 'POST'])
@login_required
def userpage_news(username, i):
    i = int(i)
    if i == 0:
        return redirect(f'/{username}/news/1')
    user = User.get(username)
    current_news = News.getPagination(i)
    if not current_news and i > 1:
        return redirect(f'/{username}/news/{i-1}')
    return render_template('news.html', user=user, news_list=current_news, page=i, curr='news')


@app.route('/<username>/protests/<i>', methods=['GET', 'POST'])
@login_required
def userpage_protests(username, i):
    i = int(i)
    if i == 0:
        return redirect(f'/{username}/protests/1')
    user = User.get(username)
    current_protests = Protest.getPagination(i)
    if not current_protests and i > 1:
        return redirect(f'/{username}/protests/{i-1}')
    return render_template('protests.html', user=user, protest_list=current_protests, page=i, curr='protests')


@app.route('/<username>/create_protest', methods=['GET', 'POST'])
@login_required
def create_new_protest(username):
    user = User.get(username)
    make_new_protest = OrganizeProtest()

    if make_new_protest.validate_on_submit():
        title = make_new_protest.title.data
        description = make_new_protest.description.data
        location = make_new_protest.location.data
        date_time = make_new_protest.date.data
        new_protest_object = Protest(name=title, description=description, location=location, date=date_time)
        user.created_protests.append(new_protest_object)
        new_protest_object.addAttendee(username)
        db.session.add(new_protest_object)
        db.session.commit()
        flash("Successfully Created a Protest")
        return redirect(f'/{username}/protests/1')

    return render_template('new_protest.html', user=user, form=make_new_protest, page=1)


@app.route('/<username>/update_my_protest/<id>', methods=['GET', 'POST'])
@login_required
def update_existing_protest(username, id):
    user = User.get(username)
    update_protest = UpdateProtest()
    curr_protest = Protest.get(id)

    if update_protest.validate_on_submit():
        curr_protest = Protest.get(id)
        title = update_protest.title.data
        description = update_protest.description.data
        location = update_protest.location.data
        date = update_protest.date.data
        if title is not None:
            curr_protest.name = title
        if description is not None:
            curr_protest.description = description
        if location is not None:
            curr_protest.location = location
        if date is not None:
            curr_protest.date = date
        flash("Successfully updated the Protest")
        return redirect(f'/{username}/protests/1')

    return render_template('update_protest.html', user=user, form=update_protest, prot=curr_protest, page=1)


@app.route('/<username>/<protest>', methods=['GET', 'POST'])
@login_required
def protest(username, protest):
    user = User.get(username)
    curr_protest = Protest.get(protest)
    return render_template('view_protest.html', user=user, protest=curr_protest)


@app.route('/<username>/<protest>/signup', methods=['GET', 'POST'])
@login_required
def signup_protest(username, protest):
    curr_protest = Protest.get(protest)
    curr_protest.addAttendee(username)
    flash(f'Successfully signed up to {curr_protest.title}!')
    return redirect(f'/{username}/protests/{1}')


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
