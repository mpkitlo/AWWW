from django.test import TestCase
from django.utils import timezone
from django.test import Client, RequestFactory
from django.urls import reverse
# from .models import User, File, Folder, FileSection, SectionType, SectionStatus, StatusData
# from .forms import FolderForm, FileForm, RegisterForm

from .views import *;
from .models import *;
from .forms import *;

import os

class ModelTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test folder
        self.folder = Folder.objects.create(
            title='Test Folder',
            description='Test folder description',
            creation_date=timezone.now(),
            owner=self.user
        )

        self.folder2 = Folder.objects.create(
            title='Test Folder',
            description='Test folder description',
            creation_date=timezone.now(),
            owner=self.user,
            parent_folder=self.folder
        )

        # Create a test file
        self.file = File.objects.create(
            title='Test File',
            description='Test file description',
            creation_date=timezone.now(),
            owner=self.user,
            parent_folder=self.folder
        )

        # Create a test file section
        self.file_section = FileSection.objects.create(
            owner=self.file,
            title='Test Section',
            description='Test section description',
            creation_date=timezone.now(),
            begin=0,
            end=10,
            data='Test section data',
            section_type=SectionType.objects.create(s_type='Test Type'),
            section_status=SectionStatus.objects.create(s_status='Test Status'),
            status_data=StatusData.objects.create(s_data='Test Data')
        )

    def test_user_model(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertIsNotNone(self.user.password)

    def test_file_model(self):
        self.assertEqual(self.file.title, 'Test File')
        self.assertEqual(self.file.description, 'Test file description')
        self.assertEqual(self.file.owner, self.user)
        self.assertEqual(self.file.parent_folder, self.folder)
        self.assertTrue(self.file.availability)
        self.assertIsNone(self.file.availability_change_date)
        self.assertIsNone(self.file.last_change_date)
        self.assertEqual(self.file.get_arr(), ['Test section data'])
        self.assertEqual(self.file.get_data(), 'Test section data')

    def test_folder_model(self):
        self.assertEqual(self.folder.title, 'Test Folder')
        self.assertEqual(self.folder.description, 'Test folder description')
        self.assertEqual(self.folder.owner, self.user)
        self.assertIsNone(self.folder.parent_folder)
        self.assertTrue(self.folder.availability)
        self.assertIsNone(self.folder.availability_change_date)
        self.assertIsNone(self.folder.last_change_date)
        self.assertTrue(self.folder.get_file_childs().exists())
        self.folder.disable_childs(timezone.now())
        self.assertTrue(self.folder.availability)
        self.assertIsNone(self.folder.availability_change_date)
        self.assertFalse(self.folder.get_folder_childs().exists())
        self.assertFalse(self.folder.get_file_childs().exists())

    def test_file_section_model(self):
        self.assertEqual(self.file_section.owner, self.file)
        self.assertEqual(self.file_section.title, 'Test Section')
        self.assertEqual(self.file_section.description, 'Test section description')
        self.assertEqual(self.file_section.begin, 0)
        self.assertEqual(self.file_section.end, 10)
        self.assertEqual(self.file_section.data, 'Test section data')
        self.assertEqual(self.file_section.section_type.s_type, 'Test Type')
        self.assertEqual(self.file_section.section_status.s_status, 'Test Status')
        self.assertEqual(self.file_section.status_data.s_data, 'Test Data')

    def test_section_type_model(self):
        section_type = SectionType.objects.create(s_type='Another Type')
        self.assertEqual(section_type.s_type, 'Another Type')

    def test_section_status_model(self):
        section_status = SectionStatus.objects.create(s_status='Another Status')
        self

class FormTestCase(TestCase):

    def test_folder_form(self):
        form_data = {
            'title': 'Test Folder',
            'description': 'Test folder description',
            'creation_date': '2023-05-26',
            'parent_folder': None
        }
        form = FolderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_file_form(self):
        form_data = {
            'title': 'Test File',
            'description': 'Test file description',
            'creation_date': '2023-05-26',
            'parent_folder': None
        }
        form = FileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        form = RegisterForm(data=form_data)


class IndexTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index_view(self):
        client = Client()
        factory = RequestFactory()

        user = User.objects.create_user(username='testuser', password='testpassword')

        url = reverse('compilator:index')
        request = factory.get(url)
        request.user = user
        response = Index(request)
        client.login(username='testuser', password='testpassword')
        response = Index(request)
        assert response.status_code == 200


        response = self.client.post(reverse('compilator:login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertRedirects(response, reverse('compilator:index'))

class OptimizationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.folder = Folder.objects.create(
            title='Test Folder',
            description='Test folder description',
            creation_date=timezone.now(),
            owner=self.user
        )
        self.file = File.objects.create(
            title='Test File',
            description='Test file description',
            creation_date=timezone.now(),
            owner=self.user,
        )
        self.file2 = File.objects.create(
            title='Test File',
            description='Test file description',
            creation_date=timezone.now(),
            owner=self.user,
        )
        self.delete = File.objects.create(
            title='Test File',
            description='Test file description',
            creation_date=timezone.now(),
            owner=self.user,
        )
        self.file_section = FileSection.objects.create(
            owner=self.file2,
            title='Test Section',
            description='Test section description',
            creation_date=timezone.now(),
            begin=0,
            end=10,
            data='3243243',
            section_type=SectionType.objects.create(s_type='Test Type'),
            section_status=SectionStatus.objects.create(s_status='Test Status'),
            status_data=StatusData.objects.create(s_data='Test Data')
        )
        self.file_section = FileSection.objects.create(
            owner=self.file,
            title='Test Section',
            description='Test section description',
            creation_date=timezone.now(),
            begin=0,
            end=10,
            data='#include <stdio.h> int main() { char a; char b; char c; char d; printf("Enter a character: "); printf("ASCII value of %c = %d", c, c); return 0; }',
            section_type=SectionType.objects.create(s_type='Test Type'),
            section_status=SectionStatus.objects.create(s_status='Test Status'),
            status_data=StatusData.objects.create(s_data='Test Data')
        )
        self.section_status = SectionStatus.objects.create(
            s_status = "kompiluje się bez ostrzeżeń"
        )
        self.section_statu2 = SectionStatus.objects.create(
            s_status = "nie kompiluję się"
        )
        self.section_statu3 = SectionStatus.objects.create(
            s_status = "kompiluje się z ostrzeżeniami"
        )
        self.section_type2 = SectionType.objects.create(s_type='dyrektywny kompilatora')
        self.section_type3 = SectionType.objects.create(s_type='procedura')
        self.section_type4 = SectionType.objects.create(s_type='deklaracje zmiennych')
        self.section_type5 = SectionType.objects.create(s_type='komentarz')
        self.section_type6 = SectionType.objects.create(s_type='wstawka asemblerowa')


    def test_optimization_view(self):
        # Create a client and request factory
        client = Client()
        factory = RequestFactory()

        # Create a POST request with the necessary data
        data = {
            'flag_0': 'O1',
            'flag_1': '',
            'flag_2': 'Os'
        }
        url = reverse('compilator:optimization')
        request = factory.post(url, data)

        # Call the view function
        response = Optimization(request)

        # Assert the redirection to the correct URL
        assert response.status_code == 302
        assert response.url == reverse('compilator:index')

        # Assert the values in the ContextContainer
        assert ContextContainer['flag_0'] == 'O1'
        assert ContextContainer['flag_1'] == ''
        assert ContextContainer['flag_2'] == 'Os'

    def test_compile_file(self):
        url = reverse('compilator:compile')
        # ContextContainer.set_file_id(self.file.id)
        xd = {}
        xd['file'] = self.file
        data = {}
        request = self.factory.post(url, data)
        response = Compile(request, xd)
        self.assertEqual(response.status_code, 302)

    # def test_compile_file2(self):
    #     url = reverse('compilator:compile')
    #     # ContextContainer.set_file_id(self.file.id)
    #     xd = {}
    #     xd['file'] = self.file2
    #     data = {}
    #     request = self.factory.post(url, data)
    #     response = Compile(request, xd)
    #     self.assertEqual(response.status_code, 302)

    def test_compile_file2(self):
        url = reverse('compilator:new_folder')
        xd = {}
        xd['file'] = self.file2
        data = {'title': 'Test Folder',
            'description': 'Test folder description',}
        request = self.factory.post(url, data)
        response = NewFolderView(request)
        self.assertEqual(response.status_code, 302)    

        request = self.factory.get(url)
        request.user = self.user
        response = NewFolderView(request)

    def test_file(self):
        url = reverse('compilator:new_file')
        request = self.factory.get(url)
        request.user = self.user
        response = NewFileView(request)

        data = {'title': 'Test File',
            'description': 'Test file description',
            'creation_date': '2023-05-26', 'data' : "dsaaaaaaaaaaaaaaaaaaaaaaaaaaasdasdasdsd"}
        request = self.factory.post(url, data)
        request.user = self.user
        response = NewFileView(request)

    def test_user_register_view(self):
        response = self.client.post(reverse('compilator:register'), {
            'username': 'newuser',
            'name': 'New User',
            'password': 'newpassword',
        })
        self.assertRedirects(response, reverse('compilator:index'))

    def test_user_register_view2(self):
        response = self.client.post(reverse('compilator:register'), {
            'username': self.user.username,
            'name': 'New User',
            'password': 'newpassword',
        })

    def test_section(self):
        url = reverse('compilator:fix_sections')
        xd = {}
        xd['file'] = self.file2
        data = {'title': 'Test Folder',
            'description': 'Test folder description',}
        request = self.factory.get(url)
        request.user = self.user
        response = FixSections(request, xd)

    def test_delete_file(self):
        url = reverse('compilator:delete_file')
        data = {'file_id' : self.delete.id}
        request = self.factory.get(url, data)
        request.user = self.user
        response = DeleteFile(request)

    def test_delete_folder(self):
        url = reverse('compilator:delete_folder')
        data = {'folder_id' : self.folder.id}
        request = self.factory.get(url, data)
        request.user = self.user
        response = DeleteFolder(request)    

    def test_download(self):

        url = reverse('compilator:download_file')
        xd = {}
        xd['asm_file'] = [["asdadd", "adasdsad"], ["asdadsad", "sdsasdads"]]
        xd['asm_name'] = 'xd'
        request = self.factory.get(url)
        request.user = self.user
        response = DownloadFile(request, xd)       


    def test_standard(self):
        url = reverse('compilator:standard')
        data = {}
        data['standard_flag'] = "xd"
        request = self.factory.post(url, data)
        request.user = self.user
        response = Standard(request)  

    def test_procesor(self):
        url = reverse('compilator:procesor')
        data = {}
        data['procesor_flag'] = "xd"
        request = self.factory.post(url, data)
        request.user = self.user
        response = Procesor(request)  
