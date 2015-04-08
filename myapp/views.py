from authen import get_user_for_id, get_user_for_eppn
from babel import dates
from collections import OrderedDict
from flask.ext.login import login_required, login_user, logout_user
from flask import render_template, abort, request, url_for, flash, \
    Markup, redirect
from flask_login import current_user
from itertools import islice
from myapp import app, login_manager, facade
from myapp.forms import LoginForm
from myapp.paginator import Pagination
from pytz import timezone

PER_PAGE = 5

TESTING = True
if TESTING:
    @app.route('/headers/')
    @login_required
    def print_headers():
        return render_template('headers.html', headers=request.headers)


@app.route('/')
@login_required
def index():
    type_list = facade.get_active_types()
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


@app.route('/instances/<instance_id>/delete', methods=['POST'])
@login_required
def delete(instance_id):
    if not facade.delete_instance(instance_id, uid=current_user.get_id()):
        abort(404)
    flash('Instance %s removed' % instance_id, 'info')
    return redirect(url_for('index'))


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
        login_user(form.user)
        flash('Logged in successfully.', 'info')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/healthcheck/')
def health_check():
    return 'Up and running', 200


@login_manager.user_loader
def user_loader(userid):
    return get_user_for_id(userid)


@login_manager.request_loader
def load_user_from_request(incoming_request):
    api_key = incoming_request.headers.get('eppn')
    if api_key:
        user = get_user_for_eppn(api_key)
        if user:
            return user
    return None


@app.template_filter('datetime')
def format_datetime(value):
    return dates.format_datetime(value,
                                 locale='en_US',
                                 tzinfo=timezone('Europe/Berlin'))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug('Error %r', error)
    return render_template('404.html'), 404


def paginate_collection(collection, page, per_page):
    instances = OrderedDict(sorted(collection.items(),
                                   key=lambda t: t[1]['ts'],
                                   reverse=True))
    return islice(instances.items(), (page - 1) * per_page, page * per_page)
