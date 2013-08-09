from werkzeug.datastructures import FileStorage

from wtforms import fields
from wtforms.fields.core import _unset_value

from . import widgets


class ModelFormField(fields.FormField):
    """
        Customized ModelFormField for MongoEngine EmbeddedDocuments.
    """
    def __init__(self, model, *args, **kwargs):
        super(ModelFormField, self).__init__(*args, **kwargs)

        self.model = model

    def populate_obj(self, obj, name):
        candidate = getattr(obj, name, None)
        if candidate is None:
            candidate = self.model()
            setattr(obj, name, candidate)

        self.form.populate_obj(candidate)


class MongoFileField(fields.FileField):
    widget = widgets.MongoFileInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super(MongoFileField, self).__init__(label, validators, **kwargs)

        self._should_delete = False

    def process(self, formdata, data=_unset_value):
        if formdata:
            marker = '_%s-delete' % self.name
            if marker in formdata:
                self._should_delete = True

        return super(MongoFileField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        field = getattr(obj, name, None)
        if field is not None:
            # If field should be deleted, clean it up
            if self._should_delete:
                field.delete()
                return

            if isinstance(self.data, FileStorage):
                if not field.grid_id:
                    func = field.put
                else:
                    func = field.replace

                func(self.data.stream,
                     filename=self.data.filename,
                     content_type=self.data.content_type)


class MongoImageField(MongoFileField):
    widget = widgets.MongoImageInput()
