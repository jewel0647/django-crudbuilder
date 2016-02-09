import crudbuilder
from six import with_metaclass
from crudbuilder.exceptions import NotModelException
from django.contrib.contenttypes.models import ContentType


class BaseBuilder(object):
    def __init__(
        self,
        app,
        model,
        crud
        ):

        self.model = model
        self.app = app
        self.crud = crud

        self.custom_modelform = self._has_crud_attr('custom_modelform')
        self.modelform_excludes = self._has_crud_attr('modelform_excludes')
        # django tables2
        self.custom_table2 = self._has_crud_attr('custom_table2')
        self.tables2_fields = self._has_crud_attr('tables2_fields')
        self.tables2_css_class = self._has_crud_attr('tables2_css_class')
        self.tables2_pagination = self._has_crud_attr('tables2_pagination')
        self.permission_required = self._has_crud_attr('permission_required')
        self.custom_templates = self._has_crud_attr('custom_templates')

    @property
    def get_model_class(self):
        """Returns model class"""
        c = ContentType.objects.get(app_label=self.app, model=self.model)
        return c.model_class()

    def _has_crud_attr(self, attr):
        if hasattr(self.crud, attr):
            return getattr(self.crud, attr)
        else:
            return None

    def view_permission(self, view_type):
        if self.permission_required:
            return self.permission_required.get(view_type, None)
        else:
            return '{}.{}_{}'.format(self.app, self.model, view_type)


class MetaCrudRegister(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(
            MetaCrudRegister, cls
            ).__new__(cls, clsname, bases, attrs)

        if bases:
            if newclass.model:
                crudbuilder.register(newclass.model, newclass)
            else:
                msg = "No model defined in {} class".format(newclass)
                raise NotModelException(msg)
        return newclass


class BaseCrudBuilder(with_metaclass(MetaCrudRegister)):
    model = None
