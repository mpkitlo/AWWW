from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    email = None
    email = models.EmailField(null=True)
    pasword2 = None
    
class File(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(User ,on_delete = models.CASCADE)
    parent_folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
    availability = models.BooleanField(default = True)      
    availability_change_date = models.DateField(null=True, blank=True)
    last_change_date = models.DateField(null=True, blank=True)

    def get_arr(self):
        arr = FileSection.objects.filter(owner = self)
        res = []
        for file in arr:
            # res.append(file.data)
            lines = (file.data).split('\n')   
            for line in lines:
                if line != "" and line != '\n':
                    res.append(line)

        return res  

    def get_data(self):
        arr = FileSection.objects.filter(owner = self)
        res = ""
        for file in arr:
            res += file.data
        return res


class Folder(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(User ,on_delete = models.CASCADE)
    parent_folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
    availability = models.BooleanField(default = True)
    availability_change_date = models.DateField(null=True, blank=True)
    last_change_date = models.DateField(null=True, blank=True)

    def get_folder_childs(self):
        return Folder.objects.filter(parent_folder = self, availability = True)

    def get_file_childs(self):
        return File.objects.filter(parent_folder = self, availability = True)

    def disable_childs(self, time):
        folders = self.get_folder_childs()
        files = self.get_file_childs()

        for file in files:
            file.availability = False
            file.availability_change_date = time
            file.save()
        for folder in folders:
            folder.availability = False
            folder.availability_change_date = time
            folder.save()
            folder.disable_childs(time)

class FileSection(models.Model):
    owner = models.ForeignKey('File', on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)   
    description = models.TextField(null=True, blank=True)         
    creation_date = models.DateTimeField()
    begin = models.IntegerField()   
    end = models.IntegerField()
    data = models.TextField()
    section_type = models.ForeignKey('SectionType', on_delete=models.CASCADE)
    section_status = models.ForeignKey('SectionStatus', null=True, blank=True, on_delete=models.CASCADE)
    status_data = models.ForeignKey('StatusData', null=True, blank=True, on_delete=models.CASCADE)
    
class SectionType(models.Model):
    s_type = models.TextField()

class SectionStatus(models.Model):
    s_status = models.TextField()

class StatusData(models.Model):
    s_data = models.TextField()
