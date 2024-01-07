import datetime

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q, Value, F, CharField
from django.db.models.functions import Concat

from account.decorators import allowed_users
from account.models import User

from .models import Thesis, Keyword, Subject, Institute, University, Type, Language

from .forms import NewThesisForm, NewInstituteForm

from .utils import numbering


@login_required(login_url='account:login')
def panel_my_theses_view(request):

    total = 0
    page = 1
    search = None
    write = False
    supervise = False
    cosupervise = False
    query:Q = Q()

    if request.method == 'POST':
        print(request.POST)
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
        
        if not request.POST.get('write') and not request.POST.get('supervise') and not request.POST.get('cosupervise'):
            write = True
        
        if request.POST.get('write'):
            write = True
            query = query | Q(author=request.user)
            
        if request.POST.get('supervise'):
            supervise = True
            query = query | Q(supervisor=request.user)
        
        if request.POST.get('cosupervise'):
            cosupervise = True
            query = query | Q(cosupervisor=request.user)
        
        if search:
            print(Thesis.objects.annotate(combined=Concat('title', Value(' '), 'abstract', Value(' '), 'institute__name', Value(' '), 'institute__university__name', output_field=CharField())).filter(Q(author=request.user) & (Q(combined__icontains=search) & query)).order_by('id').query)
            all_theses = Thesis.objects.annotate(combined=Concat('title', Value(' '), 'abstract', Value(' '), 'institute__name', Value(' '), 'institute__university__name', output_field=CharField())).filter(Q(author=request.user) & (Q(combined__icontains=search) & query)).order_by('id')
        else:
            all_theses = Thesis.objects.all().filter(Q(author=request.user) & query).order_by('id')
    else:
        all_theses = Thesis.objects.all().filter(author=request.user).order_by('id')
 

    total = len(all_theses)
    if total > 10:
        all_theses = numbering.paginate(all_theses, page)
    
    context = {
        'all_theses': all_theses,
        'write': write,
        'supervise': supervise,
        'cosupervise': cosupervise,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_theses),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_theses) == total,
        'search': search,
        'page': page
    }

    return render(request, "panel/pages/theses/my_theses.html", context)

@login_required(login_url='account:login')
def panel_thesis_detail_view(request, thesis_id):
    try:
        thesis = Thesis.objects.get(id=thesis_id)
    except Thesis.DoesNotExist:
        return redirect("panel:all_theses")
    
    
    if request.method == 'POST':
        if request.POST.get('field') == 'delete':
            thesis.delete()
            return redirect("panel:all_theses")
            
    
    

    context = {
        'thesis': thesis,
        'subjects': ", ".join(map(str, [x.heading for x in thesis.subjects.all()])),
        'keywords': ", ".join(map(str, [x.description for x in thesis.keywords.all()])),
    }

    return render(request, "panel/pages/theses/thesis_detail.html", context)

@login_required(login_url='account:login')
def panel_new_thesis_view(request):
    
    current_user:User = request.user

    if request.method == 'POST':
        print(request.POST)
        form = NewThesisForm(data = request.POST)
        if form.is_valid():
            
            thesis:Thesis = form.save(commit=False)
            
            error:bool = False
            
            try:
                thesis.supervisor = User.objects.get(username=request.POST.get('supervisor'))
            except User.DoesNotExist:
                messages.error(request, "Supervisor couldn't be found.", extra_tags="supervisor")
                error = True
            
            if request.POST.get('cosupervisor'):
                try:
                    thesis.cosupervisor = User.objects.get(username=request.POST.get('cosupervisor'))
                except User.DoesNotExist:
                    messages.error(request, "Cosupervisor couldn't be found.", extra_tags="cosupervisor")
                    error = True
            if error:
                return redirect('panel:new_thesis')
            
            thesis.author = current_user
            thesis.save()
            
            thesis.subjects.add(*[Subject.objects.get(id=s) for s in request.POST.getlist('subjects')])
            
            kwd = request.POST.get('keywords')
            
            if kwd:
                for x in list(map(str.strip, kwd.strip('][').replace('"', '').split(','))):
                    x=x.lower()
                    if Keyword.objects.filter(description=x).exists():
                        thesis.keywords.add(Keyword.objects.get(description=x))
                    else:
                        thesis.keywords.create(description=x)
                    
            
            
            return redirect('panel:thesis_detail', thesis_id=thesis.id)
        else:
            print(form.errors)
    else:
        form = NewThesisForm()
    
    context = { 'new_thesis_form': form,
               'now': str(datetime.datetime.now()),}

    return render(request, "panel/pages/theses/new_thesis.html", context)

@login_required(login_url='account:login')
def panel_edit_thesis_view(request, thesis_id):
    
    current_user:User = request.user
    
    try:
        thesis = Thesis.objects.get(pk=thesis_id)
    except Thesis.DoesNotExist:
        return redirect("panel:all_theses")

    if request.method == 'POST':
        
        
        if request.POST.get('field') == 'delete':
            thesis.delete()
            return redirect("panel:all_theses")
        
        form = NewThesisForm(data = request.POST)
        if form.is_valid():
            form.instance.sub_date = thesis.sub_date
            thesis:Thesis = form.save(commit=False)
            thesis.id = thesis_id
            
            error:bool = False
            
            try:
                thesis.supervisor = User.objects.get(username=request.POST.get('supervisor'))
            except User.DoesNotExist:
                messages.error(request, "Supervisor couldn't be found.", extra_tags="supervisorerror")
                error = True
            
            if request.POST.get('cosupervisor'):
                try:
                    thesis.cosupervisor = User.objects.get(username=request.POST.get('cosupervisor'))
                except User.DoesNotExist:
                    messages.error(request, "Cosupervisor couldn't be found.", extra_tags="cosupervisor")
                    error = True
            else:
                thesis.cosupervisor = None
            
            
            if error:
                return redirect('panel:edit_thesis', thesis_id=thesis_id)
            
            thesis.author = current_user
            thesis.save()
            
            thesis.subjects.clear()
            thesis.subjects.add(*[Subject.objects.get(id=s) for s in request.POST.getlist('subjects')])
            
            thesis.keywords.clear()
            kwd = request.POST.get('keywords')
            
            if kwd:
                for x in list(map(str.strip, kwd.strip('][').replace('"', '').split(','))):
                    x=x.lower()
                    if Keyword.objects.filter(description=x).exists():
                        thesis.keywords.add(Keyword.objects.get(description=x))
                    else:
                        thesis.keywords.create(description=x)
                    
            
            
            return redirect('panel:thesis_detail', thesis_id=thesis.id)
    else:
        form = NewThesisForm(instance=thesis)
        
    
    keywords = ", ".join(map(str, [x.description for x in thesis.keywords.all()]))
    
    context = { 'new_thesis_form': form,
               'supervisor': thesis.supervisor.username,
               'cosupervisor': thesis.cosupervisor.username if thesis.cosupervisor else '',
               'keywords': keywords,
               'thesis_id': thesis_id,}

    return render(request, "panel/pages/theses/edit_thesis.html", context)




@login_required(login_url='account:login')
def panel_all_institutes_view(request):

    total = 0
    page = 1
    search = None

    if request.method == 'POST':
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
    
    if search:
        all_institutes = Institute.objects.annotate(combined=Concat('name', Value(' '), 'university__name')).filter(combined__icontains=search).order_by('name')
    else:
        all_institutes = Institute.objects.all().order_by('name')
 

    total = len(all_institutes)
    if total > 10:
        all_institutes = numbering.paginate(all_institutes, page)
    
    context = {
        'all_insts': all_institutes,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_institutes),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_institutes) == total,
        'search': search,
        'page': page
    }

    return render(request, "panel/pages/institutes/all_institutes.html", context)

@login_required(login_url='account:login')
def panel_institute_detail_view(request, institute_id):
    try:
        institute = Institute.objects.get(id=institute_id)
    except Institute.DoesNotExist:
        return redirect("panel:all_institutes")
    
    
    if request.method == 'POST':
        if request.POST.get('field') == 'delete':
            institute.delete()
            return redirect("panel:all_institutes")
            
    
    

    context = {
        'institute': institute,
    }

    return render(request, "panel/pages/institutes/institute_detail.html", context)

@login_required(login_url='account:login')
def panel_edit_institute_view(request, institute_id):
    
    current_user:User = request.user
    
    try:
        institute = Institute.objects.get(id=institute_id)
    except Institute.DoesNotExist:
        return redirect("panel:all_institutes")

    if request.method == 'POST':
        
        if request.POST.get('field') == 'delete':
            institute.delete()
            return redirect("panel:all_institutes")
        
        form = NewInstituteForm(data = request.POST, instance=institute)
        if form.is_valid():
            
            institute:Institute = form.save()
            
            return redirect('panel:institute_detail', institute_id=institute.id)
        else:
            print(form.errors)
    else:
        form = NewInstituteForm(instance=institute)
    
    
    context = { 'new_institute_form': form,
               'institute_id': institute_id,}

    return render(request, "panel/pages/institutes/edit_institute.html", context)

@login_required(login_url='account:login')
def panel_new_institute_view(request):
    
    current_user:User = request.user

    if request.method == 'POST':
        form = NewInstituteForm(data = request.POST)
        if form.is_valid():
            
            institute:Institute = form.save()
            institute.save()
                        
            return redirect('panel:institute_detail', institute_id=institute.id)
        
    else:
        form = NewInstituteForm()
    
    context = { 'new_institute_form': form,}

    return render(request, "panel/pages/institutes/new_institute.html", context)




@login_required(login_url='account:login')
def panel_all_universities_view(request):

    total = 0
    page = 1
    search = None

    if request.method == 'POST':
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
    
    if search:
        all_universities = University.objects.filter(name__icontains=search).order_by('name')
    else:
        all_universities = University.objects.all().order_by('name')
 

    total = len(all_universities)
    if total > 10:
        all_universities = numbering.paginate(all_universities, page)
    
    context = {
        'all_unis': all_universities,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_universities),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_universities) == total,
        'search': search,
        'page': page
    }

    return render(request, "panel/pages/universities/all_universities.html", context)

@login_required(login_url='account:login')
def panel_university_detail_view(request, university_id):
    try:
        university = University.objects.get(id=university_id)
    except University.DoesNotExist:
        return redirect("panel:all_universities")
    
    
    if request.method == 'POST':
        if request.POST.get('field') == 'delete':
            university.delete()
            return redirect("panel:all_universities")
            
    
    

    context = {
        'university': university,
    }

    return render(request, "panel/pages/universities/university_detail.html", context)

@login_required(login_url='account:login')
def panel_edit_university_view(request, university_id):
    
    current_user:User = request.user
    
    try:
        university = University.objects.get(id=university_id)
    except University.DoesNotExist:
        return redirect("panel:all_universities")

    if request.method == 'POST':
        
        if request.POST.get('field') == 'delete':
            university.delete()
            return redirect("panel:all_universities")
        
        if request.POST.get('name'):
            university.name = request.POST.get('name')
            university.save()
        
            
        return redirect('panel:university_detail', university_id=university_id)
    else:
        name = university.name
    
    
    context = { 'university': university,}

    return render(request, "panel/pages/universities/edit_university.html", context)

@login_required(login_url='account:login')
def panel_new_university_view(request):
    
    current_user:User = request.user

    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        university:University = University.objects.create(name=name)
        university.save()
        
        return redirect('panel:university_detail', university_id=university.id)
    
    
    context = {}

    return render(request, "panel/pages/universities/new_university.html", context)



# TYPE CHANGE AND LIST SHOULDN'T BE AVAILABLE BY REQUIREMENTS
""" @login_required(login_url='account:login')
def panel_all_types_view(request):

    total = 0
    page = 1
    search = None

    if request.method == 'POST':
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
    
    if search:
        all_types = Type.objects.filter(name__icontains=search).order_by('name')
    else:
        all_types = Type.objects.all().order_by('name')
 

    total = len(all_types)
    if total > 10:
        all_types = numbering.paginate(all_types, page)
    
    context = {
        'all_types': all_types,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_types),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_types) == total,
        'search': search,
        'page': page
    }

    return render(request, "panel/pages/types/all_types.html", context)

@login_required(login_url='account:login')
def panel_type_detail_view(request, type_id):
    try:
        type = Type.objects.get(id=type_id)
    except Type.DoesNotExist:
        return redirect("panel:all_types")
    
    
    if request.method == 'POST':
        if request.POST.get('field') == 'delete':
            type.delete()
            return redirect("panel:all_types")
            
    
    

    context = {
        'type': type,
    }

    return render(request, "panel/pages/types/type_detail.html", context)

@login_required(login_url='account:login')
def panel_edit_type_view(request, type_id):
    
    current_user:User = request.user
    
    try:
        type = Type.objects.get(id=type_id)
    except Type.DoesNotExist:
        return redirect("panel:all_types")

    if request.method == 'POST':
        
        if request.POST.get('field') == 'delete':
            type.delete()
            return redirect("panel:all_types")
        
        if request.POST.get('name'):
            type.name = request.POST.get('name')
            type.save()
        
            
        return redirect('panel:type_detail', type_id=type_id)
    else:
        name = type.name
    
    
    context = { 'type': type,}

    return render(request, "panel/pages/types/edit_type.html", context)

@login_required(login_url='account:login')
def panel_new_type_view(request):
    
    current_user:User = request.user

    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        type:Type = Type.objects.create(name=name)
        type.save()
        
        return redirect('panel:type_detail', type_id=type.id)
    
    
    context = {}

    return render(request, "panel/pages/types/new_type.html", context)
 """



@login_required(login_url='account:login')
def panel_all_languages_view(request):

    total = 0
    page = 1
    search = None

    if request.method == 'POST':
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
    
    if search:
        all_languages = Language.objects.filter(name__icontains=search).order_by('name')
    else:
        all_languages = Language.objects.all().order_by('name')
 

    total = len(all_languages)
    if total > 10:
        all_languages = numbering.paginate(all_languages, page)
    
    context = {
        'all_languages': all_languages,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_languages),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_languages) == total,
        'search': search,
        'page': page
    }

    return render(request, "panel/pages/languages/all_languages.html", context)

@login_required(login_url='account:login')
def panel_language_detail_view(request, language_id):
    try:
        language = Language.objects.get(id=language_id)
    except Language.DoesNotExist:
        return redirect("panel:all_languages")
    
    
    if request.method == 'POST':
        if request.POST.get('field') == 'delete':
            language.delete()
            return redirect("panel:all_languages")
            
    
    

    context = {
        'language': language,
    }

    return render(request, "panel/pages/languages/language_detail.html", context)

@login_required(login_url='account:login')
def panel_edit_language_view(request, language_id):
    
    current_user:User = request.user
    
    try:
        language = Language.objects.get(id=language_id)
    except Language.DoesNotExist:
        return redirect("panel:all_languages")

    if request.method == 'POST':
        
        if request.POST.get('field') == 'delete':
            language.delete()
            return redirect("panel:all_languages")
        
        if request.POST.get('name'):
            language.name = request.POST.get('name')
            language.save()
        
            
        return redirect('panel:language_detail', language_id=language_id)
    else:
        name = language.name
    
    
    context = { 'language': language,}

    return render(request, "panel/pages/languages/edit_language.html", context)

@login_required(login_url='account:login')
def panel_new_language_view(request):
    
    current_user:User = request.user

    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        language:Language = Language.objects.create(name=name)
        language.save()
        
        return redirect('panel:language_detail', language_id=language.id)
    
    
    context = {}

    return render(request, "panel/pages/languages/new_language.html", context)


def panel_home_view(request):
    total = 0
    page = 1
    search = None

    if request.method == 'POST':
        
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
        
        if request.POST.get('search-kwd'):
            search = request.POST.get('search-kwd')
    
    if search:
        all_theses = Thesis.objects.annotate(combined=Concat('id', Value(' '), 'title', Value(' '), 'abstract', Value(' '), 'page_no', Value(' '), 'type__name', Value(' '), 'language__name', Value(' '), 'institute__name', Value(' '), 'institute__university__name', Value(' '), 'author__name', output_field=CharField())).filter(combined__icontains=search)
    else:
        all_theses = Thesis.objects.all().order_by('id')
 

    total = len(all_theses)
    if total > 10:
        all_theses = numbering.paginate(all_theses, page)
    
    context = {
        'all_theses': all_theses,
        'total': total,
        'first': ((page-1)*10)+1,
        'last': ((page-1)*10)+len(all_theses),
        'if_first': ((page-1)*10)+1 == 1,
        'if_last': ((page-1)*10)+len(all_theses) == total,
        'search': search,
        'page': page
    }
    return render(request, "panel/pages/home.html", context=context)


def panel_404_view(request, exception):
    return render(request, "panel/pages/err/404.html")