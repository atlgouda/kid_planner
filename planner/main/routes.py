from flask import render_template, request, Blueprint
from planner.models import Activity

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.order_by(Activity.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', activities=activities)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/category/<string:category>')
def category_activities(category):
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.filter(Activity.category.ilike(category))\
        .order_by(Activity.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('category_activities.html', activities=activities, category=category)