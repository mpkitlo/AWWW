from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.utils import timezone
from .models import *
from .forms import FolderForm, FileForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import logging
import os
import tempfile
import subprocess
import re

ContextContainer = {}

def Index(request):
    if not request.user.is_authenticated:
        return redirect('compilator:login')
        
    context = ContextContainer
    context['folders'] = Folder.objects.filter(parent_folder__isnull = True, availability = True, owner = request.user)  
    context['files'] = File.objects.filter(parent_folder__isnull = True, availability = True)  

    return render(request, 'pages/index.html', context)

def Standard(request):

    ContextContainer['standard_flag'] = request.POST['standard_flag']
    return redirect("compilator:index")

def Optimization(request):
    ContextContainer['flag_0'] = None
    ContextContainer['flag_1'] = None
    ContextContainer['flag_2'] = None

    if 'flag_0' in request.POST:
        ContextContainer['flag_0'] = request.POST['flag_0']
    if 'flag_1' in request.POST:
        ContextContainer['flag_1'] = request.POST['flag_1']
    if 'flag_2' in request.POST:
        ContextContainer['flag_2'] = request.POST['flag_2']
    return redirect("compilator:index")    

def Procesor(request):

    ContextContainer['procesor_flag'] = request.POST['procesor_flag']
    return redirect("compilator:index")     

def Dependant(request):

    ContextContainer['dependent_flag'] = request.POST['dependent_flag']
    return redirect("compilator:index")     

def NewFolderView(request):
    template_name = 'pages/components/new_folder.html'

    if request.method == 'POST':
        context = {}
        form = FolderForm(request.POST)

        if form.is_valid():
            pom = form.save(commit = False)
            pom.owner = request.user
            form.save()
            # return JsonResponse({'succes': True})  
        return redirect('compilator:index')   

    if request.method == 'GET':  
        ContextContainer['file'] = ""
        ContextContainer['asm_file'] = ""
        ContextContainer['asm_error'] = []      
        context = {}
        context['current_date'] = timezone.now().strftime("%Y-%m-%d %H:%M")
        context['folders2'] = Folder.objects.filter(availability = True, owner = request.user)  
        return render(request, template_name, context) 

def NewFileView(request):
    template_name = 'pages/components/new_file.html'

    if request.method == 'GET':
        ContextContainer['file'] = ""
        ContextContainer['asm_file'] = ""
        ContextContainer['asm_error'] = []
        context = {}
        context['current_date'] = timezone.now().strftime("%Y-%m-%d %H:%M")
        context['folders2'] = Folder.objects.filter(availability = True, owner = request.user)  
        return render(request, template_name, context)

    if request.method == 'POST':
        form = FileForm(request.POST)
        data = request.POST['data']

        if form.is_valid():

            file = form.save(commit = False)
            file.owner = request.user
            file.save()
            lines = data.split('\n')   

            _sekcja = FileSection()
            _sekcja.owner = file
            _sekcja.creation_date = timezone.now()
            _sekcja.begin = -1
            _sekcja.end = -1
            _sekcja.data = ""

            _begin = 1
            current_type = ""
            c_types_pattern = r"\s*\b((long\s+)?(signed\s+)?(unsigned\s+)?(short\s+)?(signed long\s+)?(unsigned long\s+)?(int|float|double|char|short)\s+(\w+|\w+\[\d+\])\s*(=\s*\S+)?\s*);\s*"
            # section_names = []

            for line in lines:
                line_type = "procedura"
                if '//' in line:
                    line_type = "komentarz"
                elif re.match(c_types_pattern ,line):
                        line_type = "deklaracje zmiennych"
                elif '#' in line:
                    line_type = "dyrektywy kompilatora"
                elif '__asm__' in line:
                    line_type = "wstawka asemblerowa"

                if len(line) == 0 or line.isspace():
                    line_type = current_type

                if current_type == line_type:
                    _sekcja.data += line + '\n'
                    _sekcja.end += 1
                else:       
                    if current_type != "":
                        _sekcja.save()
                    current_type = line_type

                    _sekcja = FileSection()
                    _sekcja.owner = file
                    _sekcja.creation_date = timezone.now()
                    _sekcja.section_type = SectionType.objects.get(s_type = current_type)
                    _sekcja.begin = _begin
                    _sekcja.end = _begin
                    _sekcja.data = line + '\n'

                _begin += 1    

            if _sekcja.data != "":
                _sekcja.end += 1
                _sekcja.save()
                _sekcja.begin = -1
                _sekcja.end = -1
                _sekcja.data = ""            

            ContextContainer['file'] = file

            # redirect_url = reverse('compilator:fix_sections')
            # return JsonResponse({"redirect": redirect_url})
            return redirect('compilator:fix_sections')


def Register(request):
    ContextContainer = {}
    if request.method == 'GET':
        return render(request, 'pages/register.html')
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return render(request, 'pages/register.html', {'error' : 'Taki login już istnieje!'})                   # ten sam POST request przy odświeżaniu strony

        password = request.POST['password']

        user = User(username=username)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('compilator:index')

def Login(request):
    ContextContainer = {}
    if request.method == 'GET':
        return render(request, 'pages/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('compilator:index')

        return render(request, 'pages/login.html', {'error' : 'Login lub hasło błędne!'})      

def Logout(request):
    logout(request)
    return redirect('compilator:login')                   

def ShowFile(request):
    file_id = request.GET['file_id']
    # ContextContainer.reset()
    ContextContainer['file'] = File.objects.get(id = file_id)
    ContextContainer['asm_file'] = ""
    ContextContainer['asm_error'] = []
    # context = ContextContainer.get_context()
    # ContextContainer.add('file_id', file_id)
    # ContextContainer.add('asm_file', None)
    # ContextContainer.add('asm_error', None)

    return redirect('compilator:index')


def Compile(request, context = ContextContainer):
    # context = ContextContainer
    # logger = logging.getLogger(__name__)
    # logger.debug(context)
    if 'file' not in context:
        return redirect('compilator:index')    

    with open('temp_file.c', 'w') as f:
        f.write(context['file'].get_data())

    compilation_settings = ['sdcc', '-S']

    if 'standard_flag' in context and context['standard_flag'] != None:
        compilation_settings.append(f"--std-{context['standard_flag']}".lower())

    if 'procesor_flag' in context and context['procesor_flag'] != None:  
        compilation_settings.append(f"-m{context['procesor_flag']}".lower())

    for flag in ['flag_0', 'flag_1', 'flag_2']:
        if flag in context and context[flag] != None:
            compilation_settings.append(f"--{context[flag]}")
    if 'dependent_flag' in context and context['dependent_flag'] != None:
        compilation_settings.append(f"--{context['dependent_flag']}")   

    compilation_settings.append('temp_file.c')    

    result = subprocess.run(compilation_settings, capture_output=True, text=True)
    stderr = result.stderr

    file_sections = FileSection.objects.filter(owner = context['file'].id)

    for section in file_sections:
        section.section_status = SectionStatus.objects.get(s_status = "kompiluje się bez ostrzeżeń")
        section.save()
        
    # ContextContainer['asm_error'] = stderr
    ContextContainer['asm_error'] = []
    lines = stderr.split('\n')
    for line in lines:
        ContextContainer['asm_error'].append(line)
        if "error" in line:
            match = re.search(r'\d+', line).group()
            if match:     
                # logger = logging.getLogger(__name__)
                # logger.debug(int(match))
                file_section = FileSection.objects.filter(owner = context['file'].id).get(begin__lte=(int(match)), end__gte=(int(match)))
                file_section.section_status = SectionStatus.objects.get(s_status = "nie kompiluję się")
                _status_data = StatusData()
                _status_data.s_data = line
                _status_data.save()
                file_section.status_data = _status_data
                file_section.save()
        elif "warning" in line: 
            match = re.search(r'\d+', line).group()
            if match:   
                file_section = FileSection.objects.filter(owner = context['file'].id).get(begin__lte=(int(match)), end__gte=(int(match)))
                file_section.section_status = SectionStatus.objects.get(s_status = "kompiluje się z ostrzeżeniami")
                _status_data = StatusData()
                _status_data.s_data = line
                _status_data.save()
                file_section.status_data = _status_data
                file_section.save()

    if os.path.exists('temp_file.asm'):
        with open('temp_file.asm', 'r') as f:
            data_file = f.read()

            result1 = []
            result2 = []
            temp1 = ''  
            temp2 = ''
            counter = 0
            iterator = 0
            lines = data_file.split('\n')

            for line in lines:
                if re.match(r'^;-', line):
                    if counter == 0:
                        if iterator != 0:
                            result2.append(temp2)
                        temp2 = ''
                        temp1 += line + '\n'
                        counter = 1
                    else:
                        if counter == 1:
                            temp1 += line
                            result1.append(temp1)
                            counter = 0
                            temp1 = ''
                elif re.match(r'^;\s*-', line):
                    if counter == 1:
                        temp1 += line + '\n'
                        counter = 2
                    else:
                        if counter == 2:
                            temp1 += line
                            result1.append(temp1)
                            counter = 0
                            temp1 = ''
                else:
                    if counter == 2:
                        temp1 += line + '\n'
                    if counter == 1:
                        temp1 += line + '\n'
                    if counter == 0:
                        temp2 += line + '\n'
                iterator += 1        

            result1.append(temp1)
            result2.append(temp2)

            result = []
            for a, b in zip(result1, result2):
                x = []
                x.append(a)
                x.append(b)
                result.append(x)

            # ContextContainer.add('asm_file', result)
            ContextContainer['asm_file'] = result
            # ContextContainer.add('asm_name', context['file'].title)
            ContextContainer['asm_name'] = context['file'].title

        os.remove('temp_file.asm')

    else:
        # ContextContainer.add('asm_file', None)
        ContextContainer['asm_file'] =  ""

    os.remove('temp_file.c')  

    ContextContainer['standard_flag'] =  None
    ContextContainer['procesor_flag'] =  None
    ContextContainer['dependent_flag'] = None
    ContextContainer['flag_0'] = None
    ContextContainer['flag_1'] = None
    ContextContainer['flag_2'] = None

    return redirect('compilator:index')  

def FixSections(request, context = ContextContainer ):
    template_name = 'pages/components/fix_sections.html'
    if 'file' not in context and context['file'] != "":
        return redirect('compilator:index')        

    if request.method == 'GET':
        section_names = []
        for section in FileSection.objects.filter(owner = context['file']): 
            section_names.append(section.section_type.s_type)
        context['sections'] = zip(section_names, FileSection.objects.filter(owner = context['file']))
        context['section_types'] =  SectionType.objects.all()

        return render(request, template_name, context)

    if request.method == 'POST':
        type_names = []
        for i in SectionType.objects.all():
            type_names.append(i.s_type)
        for key, value in request.POST.items():    
            if key != 'csrfmiddlewaretoken' and value not in type_names:
                pom = FileSection.objects.get(id = key)
                pom.data = value
                pom.save()
            elif value in type_names:
                key2 = key[:-1]
                pom2 = FileSection.objects.get(id = key2)
                pom2.section_type = SectionType.objects.get(s_type = value)
                pom2.save()

        # return redirect('compilator:index')  
        redirect_url = reverse('compilator:index')
        return JsonResponse({"redirect": redirect_url}) 


def DeleteFile(request):
    file_id = request.GET['file_id']
    time = timezone.now()
    file = File.objects.get(id = file_id) 
    if(file.parent_folder):
        file.parent_folder.availability_change_date = time 
    file.availability = False
    file.availability_change_date = time   
    file.save()
    ContextContainer['file'] = None
    ContextContainer['asm_file'] = None
    ContextContainer['asm_error'] = []

    return redirect('compilator:index')   

def DeleteFolder(request):
    folder_id = request.GET['folder_id']
    time = timezone.now()
    folder = Folder.objects.get(id = folder_id)
    folder.availability = False
    folder.availability_change_date = time
    folder.save()
    folder.disable_childs(time)

    return redirect('compilator:index')       


def DownloadFile(request, context = ContextContainer):
    
    if 'asm_file' not in context or context['asm_file'] == "":
        return redirect('compilator:index')

    file_content = context['asm_file']
    asm_file = ""
    for f1, f2 in file_content:
        asm_file += f1 + '\n'
        asm_file += f2

    response = HttpResponse(asm_file, content_type='text/plain')
    response['Content-Disposition'] = f"{context['asm_name']}"
    return response    