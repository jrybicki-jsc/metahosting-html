from authen import get_user_for_name, get_user_for_id
from babel import dates
from collections import OrderedDict
from facade import facade
from flask.ext.login import login_required, login_user, logout_user
from flask import render_template, abort, request, url_for, flash, \
    Markup, redirect
from flask_login import current_user
from itertools import islice
from myapp import app, login_manager
from myapp.forms import LoginForm
from myapp.paginator import Pagination
from pytz import timezone

PER_PAGE = 5


@app.route('/')
@login_required
def index():
    type_list = facade.get_types()
    return render_template('index.html', types=type_list)


@app.route('/', methods=['POST'])
@login_required
def create_form():
    instance_type = request.form['instance_type']
    instance = facade.create_instance(instance_type, current_user.get_id())
    if instance is None:
        flash('Unable to create instance', 'error')
    else:
        message = Markup('Instance <a href="%s">%s</a> created' %
                         (url_for('one_instance', instance_id=instance['id']),
                          instance['id']))

        flash(message, 'info')
    return render_template('index.html', types=facade.get_types())


@app.route('/instances/')
@login_required
def all_instances():
    page = int(request.args.get('page', '1'))
    instances = facade.get_all_instances(uid=current_user.get_id())
    count = len(instances)
    instances = paginate_collection(instances, page, PER_PAGE)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('instances.html', instances=instances,
                           pagination=pagination)


@app.route('/instances/<instance_id>')
@login_required
def one_instance(instance_id):
    instance = facade.get_instance(instance_id=instance_id,
                                   uid=current_user.get_id())
    if instance is None:
        abort(404)

    return render_template('single_instance.html', id=instance_id,
                           instance=instance)


@app.route('/types/')
def all_types():
    type_list = facade.get_types()
    return render_template('types.html', types=type_list)


@app.route('/types/<name>')
@login_required
def one_type(name):
    types = facade.get_types()
    if name not in types:
        abort(404)

    instances = facade.get_instances_of_type(instance_type_name=name,
                                             uid=current_user.get_id())
    return render_template('single_type.html', type_name=name,
                           type_description=types[name],
                           instances=instances)


@app.route('/help/')
@app.route('/help/<subject>', defaults={'subject': 'General'})
def help_page(subject='General'):
    return render_template('help.html', subject=subject)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_for_name(form.username.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'info')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Unable to validate password', 'warning')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))


@login_manager.user_loader
def user_loader(userid):
    return get_user_for_id(userid)


# @login_manager.request_loader
# def load_user_from_request(incoming_request):
# api_key = incoming_request.headers.get('API-KEY')
# if api_key:
# user = get_user_for_api_key(api_key)
#         if user:
#             return user
#     return None


@app.template_filter('datetime')
def format_datetime(value):
    return dates.format_datetime(value,
                                 locale='en_US',
                                 tzinfo=timezone('Europe/Berlin'))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug('Error %r' % error)
    return render_template('404.html'), 404


def paginate_collection(collection, page, per_page):
    instances = OrderedDict(collection)
    return islice(instances.items(), (page - 1) * per_page, page * per_page)
