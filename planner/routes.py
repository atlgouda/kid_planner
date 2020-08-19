import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from planner import app, db, bcrypt
from planner.forms import RegistrationForm, LoginForm, UpdateAccountForm, ActivityForm
from planner.models import User, Activity
from flask_login import login_user, current_user, logout_user, login_required

# activities = [
#     {
#         'title': 'Dino Rescue',
#         'link': 'https://www.instagram.com/p/CC_4a-2lBgM/',
#         'description': '"save" dinos from lage bowl of rice',
#         'category': 'Science',
#         'date_posted': 'Aug 2, 2020'
#     },
#     {
#         'title': 'Potions',
#         'link': 'https://www.instagram.com/p/CCmHb9Plva-/',
#         'description': 'vinegar, shaving cream, dish soap (washing up liquid) and baking soda (bi-carb).',
#         'category': 'Science',
#         'date_posted': 'Aug 2, 2020'
#     }
# ]

@app.route('/')
def home():
    activities = Activity.query.all()
    return render_template('home.html', activities=activities)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account.html', title='Account', 
                                image_file=image_file, form=form)


@app.route('/activity/new', methods=['GET', 'POST'])
@login_required
def new_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.title.data, description=form.description.data, link = form.link.data, category=form.category.data, author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your activity has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_activity.html', title='New Activity', form = form, legend='New Activity')

@app.route("/activity/<int:activity_id>")
def activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template('activity.html', title=activity.title, activity=activity)

@app.route("/activity/<int:activity_id>/update", methods=['GET', 'POST'])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.author != current_user:
        abort(403)
    form = ActivityForm()
    if form.validate_on_submit():
        activity.title = form.title.data
        activity.description = form.description.data
        activity.link = form.link.data
        activity.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('activity', activity_id=activity.id))
    elif request.method == 'GET':
        form.title.data = activity.title
        form.description.data = activity.description
        form.link.data = activity.link
        form.category.data = activity.category
    return render_template('create_activity.html', title='Update Activity', form=form, legend='Update Activity')

@app.route("/activity/<int:activity_id>/delete", methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.author != current_user:
        abort(403)
    db.session.delete(activity)
    db.session.commit()
    flash('Your activity has been deleted!', 'success')
    return redirect(url_for('home'))