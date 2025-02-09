from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone



def load_departments(request):
    institute_id = request.GET.get("institute_id")
    departments = Dept.objects.filter(institute_id=institute_id).values('id', 'department')
    return JsonResponse(list(departments), safe=False)

def load_batches(request):
    institute_id = request.GET.get("institute_id")
    department_id = request.GET.get('department_id')
    batches = Batch.objects.filter(institute_id=institute_id, department_id=department_id).values('id', 'batch')
    return JsonResponse(list(batches), safe=False)

def load_sections(request):
    institute_id = request.GET.get('institute_id')
    department_id = request.GET.get('department_id')
    batch_id = request.GET.get('batch_id')
    sections = Section.objects.filter(
        institute_id=institute_id,
        department_id=department_id,
        batch_id=batch_id
    ).values('id', 'section')
    return JsonResponse(list(sections), safe=False)

def home(request):
    institutes = Institute.objects.all()
    return render(request, "home.html", {"institutes": institutes})





def routine_page(request, institute, dept, batch, section):
    # Convert URL parameters (hyphenated) to match database fields
    institute_name = institute.replace('-', ' ')
    dept_name = dept.replace('-', '-')
    batch_name = batch.replace('-', '-')
    section_name = section.replace('-', ' ')
    
    # Fetch the corresponding objects
    institute_obj = get_object_or_404(Institute, name__iexact=institute_name)
    dept_obj = get_object_or_404(Dept, institute=institute_obj, department__iexact=dept_name)
    batch_obj = get_object_or_404(Batch, institute=institute_obj, department=dept_obj, batch__iexact=batch_name)
    section_obj = get_object_or_404(Section, institute=institute_obj, department=dept_obj, batch=batch_obj, section__iexact=section_name)
    
    # Get notices, exams, and routine related to this section
    thirty_days_ago = timezone.now() - timedelta(days=30)
    notices = Notices.objects.filter(section=section_obj, notice_date__gte = thirty_days_ago).order_by("-notice_date")
    exams = Exams.objects.filter(section=section_obj, exam_date__gte=timezone.now()).order_by("exam_date")
    today_name = datetime.today().strftime("%A")
    current_time = datetime.now().time()
    today_all = datetime.today().strftime("%A, %d %b %Y")
    
    all_classes = Classes.objects.filter(section=section_obj, day__name=today_name).order_by("start_time")
    next_class = all_classes.filter(start_time__gt=current_time, paused = False).first()
    next_class_time_js = f"{datetime.today().date()} {next_class.start_time}" if next_class else None
    
    # Process exam and notice dates for display
    for cls in all_classes:
        cls.end_time_display = cls.end_time
    for ex in exams:
        ex.ex_date = ex.exam_date.strftime("%d %b")
    for notice in notices:
        notice.ndate = notice.notice_date.strftime("%d %b")
    
    return render(request, "routine.html", {
        "all_classes": all_classes, 
        "next_class_time_js": next_class_time_js,
        "today_all": today_all,
        "exams": exams,
        "notices": notices,
        "section": section_obj
    })
