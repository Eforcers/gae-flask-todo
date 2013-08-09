from nose.tools import eq_, ok_
from nose.plugins.skip import SkipTest

# Skip test on PY3
from flask.ext.admin._compat import PY2
if not PY2:
    raise SkipTest('MongoEngine is not Python 3 compatible')

from wtforms import fields

from flask.ext.admin import form
from flask.ext.admin.contrib.mongoengine import ModelView

from . import setup


class CustomModelView(ModelView):
    def __init__(self, model,
                 name=None, category=None, endpoint=None, url=None,
                 **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        super(CustomModelView, self).__init__(model,
                                              name, category,
                                              endpoint, url)


def create_models(db):
    class Model1(db.Document):
        test1 = db.StringField(max_length=20)
        test2 = db.StringField(max_length=20)
        test3 = db.StringField()
        test4 = db.StringField()

    class Model2(db.Document):
        int_field = db.IntField()
        bool_field = db.BooleanField()

    Model1.objects.delete()
    Model2.objects.delete()

    return Model1, Model2


def test_model():
    app, db, admin = setup()

    Model1, Model2 = create_models(db)

    view = CustomModelView(Model1)
    admin.add_view(view)

    eq_(view.model, Model1)
    eq_(view.name, 'Model1')
    eq_(view.endpoint, 'model1view')

    eq_(view._primary_key, 'id')

    ok_('test1' in view._sortable_columns)
    ok_('test2' in view._sortable_columns)
    ok_('test3' in view._sortable_columns)
    ok_('test4' in view._sortable_columns)

    ok_(view._create_form_class is not None)
    ok_(view._edit_form_class is not None)
    eq_(view._search_supported, False)
    eq_(view._filters, None)

    # Verify form
    # TODO: Figure out why there's inconsistency
    try:
        eq_(view._create_form_class.test1.field_class, fields.TextField)
        eq_(view._create_form_class.test2.field_class, fields.TextField)
    except AssertionError:
        eq_(view._create_form_class.test1.field_class, fields.StringField)
        eq_(view._create_form_class.test2.field_class, fields.StringField)

    eq_(view._create_form_class.test3.field_class, fields.TextAreaField)
    eq_(view._create_form_class.test4.field_class, fields.TextAreaField)

    # Make some test clients
    client = app.test_client()

    rv = client.get('/admin/model1view/')
    eq_(rv.status_code, 200)

    rv = client.get('/admin/model1view/new/')
    eq_(rv.status_code, 200)

    rv = client.post('/admin/model1view/new/',
                     data=dict(test1='test1large', test2='test2'))
    eq_(rv.status_code, 302)

    model = Model1.objects.first()
    eq_(model.test1, 'test1large')
    eq_(model.test2, 'test2')
    eq_(model.test3, '')
    eq_(model.test4, '')

    rv = client.get('/admin/model1view/')
    eq_(rv.status_code, 200)
    ok_('test1large' in rv.data)

    url = '/admin/model1view/edit/?id=%s' % model.id
    rv = client.get(url)
    eq_(rv.status_code, 200)

    rv = client.post(url,
                     data=dict(test1='test1small', test2='test2large'))
    eq_(rv.status_code, 302)

    model = Model1.objects.first()
    eq_(model.test1, 'test1small')
    eq_(model.test2, 'test2large')
    eq_(model.test3, '')
    eq_(model.test4, '')

    url = '/admin/model1view/delete/?id=%s' % model.id
    rv = client.post(url)
    eq_(rv.status_code, 302)
    eq_(Model1.objects.count(), 0)


def test_default_sort():
    app, db, admin = setup()
    M1, _ = create_models(db)

    M1(test1='c').save()
    M1(test1='b').save()
    M1(test1='a').save()

    eq_(M1.objects.count(), 3)

    view = CustomModelView(M1, column_default_sort='test1')
    admin.add_view(view)

    _, data = view.get_list(0, None, None, None, None)

    eq_(data[0].test1, 'a')
    eq_(data[1].test1, 'b')
    eq_(data[2].test1, 'c')


def test_extra_fields():
    app, db, admin = setup()

    Model1, _ = create_models(db)

    view = CustomModelView(
        Model1,
        form_extra_fields={
            'extra_field': fields.TextField('Extra Field')
        }
    )
    admin.add_view(view)

    client = app.test_client()

    rv = client.get('/admin/model1view/new/')
    eq_(rv.status_code, 200)

    # Check presence and order
    data = rv.data.decode('utf-8')
    ok_('Extra Field' in data)
    pos1 = data.find('Extra Field')
    pos2 = data.find('Test1')
    ok_(pos2 < pos1)


def test_extra_field_order():
    app, db, admin = setup()

    Model1, _ = create_models(db)

    view = CustomModelView(
        Model1,
        form_columns=('extra_field', 'test1'),
        form_extra_fields={
            'extra_field': fields.TextField('Extra Field')
        }
    )
    admin.add_view(view)

    client = app.test_client()

    rv = client.get('/admin/model1view/new/')
    eq_(rv.status_code, 200)

    # Check presence and order
    data = rv.data.decode('utf-8')
    pos1 = data.find('Extra Field')
    pos2 = data.find('Test1')
    ok_(pos2 > pos1)


def test_custom_form_base():
    app, db, admin = setup()

    class TestForm(form.BaseForm):
        pass

    Model1, _ = create_models(db)

    view = CustomModelView(
        Model1,
        form_base_class=TestForm
    )
    admin.add_view(view)

    ok_(hasattr(view._create_form_class, 'test1'))

    create_form = view.create_form()
    ok_(isinstance(create_form, TestForm))
