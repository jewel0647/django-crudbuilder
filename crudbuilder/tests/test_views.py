from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from crudbuilder.tests.models import TestModel
from crudbuilder.tests.crud import TestModelCrud
from crudbuilder.tests.forms import TestModelForm
from crudbuilder.tests.tables import TestModelTable


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        TestModelCrud.custom_modelform = TestModelForm
        TestModelCrud.custom_table2 = TestModelTable

        self.user = User.objects.create_user(
            username='asdf',
            password='asdf3452',
            email='sa@me.org')

    def client_login(self):
        self.client.login(
            username=self.user.username,
            password='asdf3452'
        )

    def get_list_view(self):
        self.client_login()
        response = self.client.get(reverse('tests-testmodel-list'))
        self.assertEqual(200, response.status_code)

    def test_user_not_logged_in(self):
        response = self.client.get(reverse('tests-testmodel-list'))
        self.assertEqual(302, response.status_code)

    def tearDown(self):
        TestModelCrud.custom_table2 = None
        TestModelCrud.custom_modelform = None
        TestModelCrud.createupdate_forms = None

    def test_user_logged_in(self):
        self.get_list_view()

    def test_view_with_default_form(self):
        TestModelCrud.custom_modelform = None
        self.get_list_view()

    def test_view_with_default_tables2(self):
        TestModelCrud.custom_table2 = None
        self.get_list_view()

    def test_invalid_entry_create(self):
        self.client_login()
        data = {'name': 'Test text', 'email': 'same.org'}
        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "email", "Enter a valid email address.")

    def test_valid_entry_create(self):
        self.client_login()
        data = {'name': 'Test text', 'email': 'sa@me.org'}
        self.assertEqual(TestModel.objects.count(), 0)

        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TestModel.objects.count(), 1)

        response = self.client.post('/crud/tests/testmodels/1/update/', data)
        self.assertEqual(response.status_code, 302)

    @override_settings(PERMISSION_REQUIRED_FOR_CRUD=True)
    def test_permission_required_enabled(self):
        self.client_login()
        response = self.client.get('/crud/tests/testmodels/')
        self.assertEqual(302, response.status_code)

    def test_search_list(self):
        self.client_login()
        response = self.client.get('/crud/tests/testmodels/?search=some_text')
        self.assertEqual(200, response.status_code)

    @override_settings(LOGIN_REQUIRED_FOR_CRUD=False)
    def test_no_login(self):
        response = self.client.get(reverse('tests-testmodel-list'))
        self.assertEqual(200, response.status_code)

    def test_separate_createupdateform(self):
        TestModelCrud.custom_modelform = None
        TestModelCrud.createupdate_forms = dict(
            create=TestModelForm,
            update=TestModelForm)

        self.client_login()
        data = {'name': 'Test text', 'email': 'sa@me.org'}
        self.assertEqual(TestModel.objects.count(), 0)

        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TestModel.objects.count(), 1)

        response = self.client.post('/crud/tests/testmodels/1/update/', data)
        self.assertEqual(response.status_code, 302)

    def test_custom_queryset(self):
        def custom_queryset(self, request, **kwargs):
            return self.model.objects.all()
        setattr(TestModelCrud, 'custom_queryset', custom_queryset)
        self.get_list_view()
