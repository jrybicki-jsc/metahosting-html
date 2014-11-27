from collections import OrderedDict
from itertools import islice
from flask.ext.login import login_required, login_user
from flask_login import current_user, logout_user
from werkzeug.utils import redirect
from myapp import app, login_manager
from flask import render_template, abort, request, url_for, flash, g
from facade import get_all_instances, get_types, get_instance, \
    get_instances_of_type, create_instance
from babel import dates
from myapp.forms import LoginForm
from myapp.paginator import Pagination
from myapp.user import User, get_user_for_id, get_user_for_name

PER_PAGE = 5


@app.route('/')
@login_required
def index():
    type_list = get_types()
    return render_template('index.html', types=type_list)


@app.route('/', methods=['POST'])
@login_required
def create_form():
    instance_type = request.form['instance_type']
    instance = create_instance(instance_type)
    return render_template('instance_created.html', id=instance['id'],
                           instance=instance)



@app.route('/instances/')
@login_required
def all_instances():
    page = int(request.args.get('page', '1'))
    count = len(get_all_instances())
    instances = paginate_collection(get_all_instances(), page, PER_PAGE)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('instances.html', instances=instances,
                           pagination=pagination)


@app.route('/instances/<instance_id>')
@login_required
def one_instance(instance_id):
    instance = get_instance(instance_id=instance_id)
    if instance is None:
        abort(404)

    return render_template('single_instance.html', id=instance_id,
                           instance=instance)


@app.route('/types/')
def all_types():
    type_list = get_types()
    return render_template('types.html', types=type_list)


@app.route('/types/<name>')
@login_required
def one_type(name):
    types = get_types()
    if name in types:
        instances = get_instances_of_type(instance_type_name=name)
        return render_template('single_type.html', type_name=name,
                               type_description=types[name],
                               instances=instances)
    abort(404)


@app.route('/help/<subject>', defaults={'subject': 'General'})
def help_page(subject):
    return render_template('help.html', subject=subject)


@app.route('/settings/')
@login_required
def settings():
    if current_user.is_authenticated():
        return 'oo %s' % current_user.get_name()


@login_manager.user_loader
def user_loader(userid):
    return get_user_for_id(userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if g.user is not None and g.user.is_authenticated():
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_for_name(form.username.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.template_filter('datetime')
def format_datetime(value):
    return dates.format_datetime(value)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug('Error %r' % error)
    return render_template('404.html'), 404


def paginate_collection(collection, page, per_page):
    instances = OrderedDict(collection)
    return islice(instances.items(), (page - 1) * per_page, page * per_page)
