from flask import render_template, url_for, flash, redirect
from planner import app
from planner.forms import RegistrationForm, LoginForm
from planner.models import User, Activity

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)