from flask import render_template, url_for, flash, redirect, request
from planner import app, db, bcrypt
from planner.forms import RegistrationForm, LoginForm, UpdateAccountForm
from planner.models import User, Activity
from flask_login import login_user, current_user, logout_user, login_required

activities = [
    {
        'title': 'Dino Rescue',
        'link': 'https://www.instagram.com/p/CC_4a-2lBgM/',
        'description': '"save" dinos from lage bowl of rice',
        'category': 'Science',
        'date_posted': 'Aug 2, 2020'
    },
    {
        'title': 'Potions',
        'link': 'https://www.instagram.com/p/CCmHb9Plva-/',
        'description': 'vinegar, shaving cream, dish soap (washing up liquid) and baking soda (bi-carb).',
        'category': 'Science',
        'date_posted': 'Aug 2, 2020'
    }
]

@app.route('/')
def home():
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

@app.route('/account')
@login_required
def account():
        form = UpdateAccountForm()
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account.html', title='Account', 
                                image_file=image_file, form=form)
