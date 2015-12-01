from crudbuilder.abstract import BaseCrudBuilder
from example.models import Person, PersonEmployment
from example.forms import PersonEmploymentForm


class PersonCrud(BaseCrudBuilder):
    model = Person
    search_feilds = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    modelform_excludes = ['created_by', 'updated_by']

    # custom_templates = {
    #     'list': 'yourtemplates/template.html'
    # }

    # permission_required = {
    #     'list': 'example.person_list',
    #     'create': 'example.person_create'
    # }


class PersonEmploymentCrud(BaseCrudBuilder):
    model = PersonEmployment
    tables2_fields = ('year', 'salary', 'medical_allowance')
    search_feilds = ['year', 'person__name']
    tables2_css_class = "table table-bordered table-condensed"
    custom_modelform = PersonEmploymentForm
    # modelform_excludes = ['person']
