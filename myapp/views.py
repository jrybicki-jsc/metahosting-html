from myapp import app
from flask import render_template, abort, request
from facade import get_all_instances, get_types, get_instance, \
    get_instances_of_type, create_instance, get_instances_for_page
from babel import dates
from myapp.paginator import Pagination

PER_PAGE = 5


@app.route('/')
def index():
    type_list = get_types()
    return render_template('index.html', types=type_list)


@app.route('/', methods=['POST'])
def create_form():
    # {% for id,instance in instances.iteritems() %}
    instance_type = request.form['instance_type']
    instance = create_instance(instance_type)
    return render_template('instance_created.html', id=instance['id'],
                           instance=instance)



@app.route('/instances/')
def all_instances():
    page = int(request.args.get('page', '1'))
    count = len(get_all_instances())
    instances = get_instances_for_page(page, PER_PAGE)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('instances.html', instances=instances,
                           pagination=pagination)


@app.route('/instances/<instance_id>')
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


@app.template_filter('datetime')
def format_datetime(value):
    return dates.format_datetime(value)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
