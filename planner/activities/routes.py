from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from planner import db
from planner.models import Activity
from planner.activities.forms import ActivityForm

activities = Blueprint('activities', __name__)

@activities.route('/activity/new', methods=['GET', 'POST'])
@login_required
def new_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.title.data, description=form.description.data, link = form.link.data, category=form.category.data, author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your activity has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_activity.html', title='New Activity', form = form, legend='New Activity')

@activities.route("/activity/<int:activity_id>")
def activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template('activity.html', title=activity.title, activity=activity)

@activities.route("/activity/<int:activity_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('activities.activity', activity_id=activity.id))
    elif request.method == 'GET':
        form.title.data = activity.title
        form.description.data = activity.description
        form.link.data = activity.link
        form.category.data = activity.category
    return render_template('create_activity.html', title='Update Activity', form=form, legend='Update Activity')

@activities.route("/activity/<int:activity_id>/delete", methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.author != current_user:
        abort(403)
    db.session.delete(activity)
    db.session.commit()
    flash('Your activity has been deleted!', 'success')
    return redirect(url_for('main.home'))
