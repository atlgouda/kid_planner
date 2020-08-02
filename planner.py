from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm
import email_validator

app = Flask(__name__)

app.config['SECRET_KEY']='10eba29c88131580215be7db2c58c78c'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    activities = db.relationship('Activity', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Actifity('{self.title}', '{self.date_posted}')"

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

if __name__ == '__main__':
    app.run(debug=True)