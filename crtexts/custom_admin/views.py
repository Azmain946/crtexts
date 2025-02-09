from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from new_routine.models import *
from django.contrib import admin, messages
from datetime import datetime, timedelta
from .forms import *
from django.utils import timezone



@login_required
def cancel_class(request, class_id):
    user = request.user
    class_obj = get_object_or_404(Classes, id=class_id)
    section = Section.objects.filter(class_representative = user).first()
    if user == section.class_representative:
        print("before:", class_obj.paused)
        if (class_obj.paused) == False:
            class_obj.paused = True
            class_obj.save()
        else:
            class_obj.paused = False
            class_obj.save()
        print("after:", class_obj.paused)
        return redirect('custom_dashboard')

@login_required

def add_notice(request):
    user = request.user

    section = Section.objects.filter(class_representative = user).first()

    if not section:
        return redirect('custom_dashboard')
    
    if request.method == "POST":
        form = CreateNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.section = section
            notice.save()

            return redirect('custom_dashboard')
        else:
            print(form.errors)
    else:
        form = CreateNoticeForm()

    return render(request, 'custom_admin/add_notice.html', {
        'form': form,
        'assigned_section': section,
    })

@login_required
def update_notice(request, notice_id):
    notice_obj = get_object_or_404(Notices, id=notice_id)
    assigned_section = Section.objects.filter(class_representative=request.user).first()

    if not assigned_section:
        return redirect('custom_dashboard')

    if request.method == "POST":
        form = UpdateNoticeForm(request.POST, instance=notice_obj)
        if form.is_valid():
            form.save()  # Save the form instance
            messages.success(request, "Notice updated successfully")
            return redirect('custom_dashboard')
        else:
            print("Form errors:", form.errors)  # Check for any form validation errors
    else:
        form = UpdateNoticeForm(instance=notice_obj)

    return render(request, 'custom_admin/change_notice.html', {
        'form': form,
        'notice_obj': notice_obj,
        'assigned_section': assigned_section,
    })

@login_required
def delete_notice(request, notice_id):
    notice_obj = get_object_or_404(Notices, id=notice_id)

    if request.user == notice_obj.section.class_representative:
        notice_obj.delete()
        messages.success(request, "Notice deleted successfully")
    else:
        messages.error(request, "You don't have permission to delete this notice.")

    return redirect('custom_dashboard')


@login_required
def add_exam(request):
    user = request.user

    section = Section.objects.filter(class_representative=user).first()
    if not section:
        return redirect('custom_dashboard')
    
    if request.method == "POST":
        form = ExamCreateForm(request.POST, user=user)  # Pass the user as a keyword argument
        if form.is_valid():
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            # Convert to timedelta
            exam_duration = timedelta(hours=hours, minutes=minutes)
            print("Class Duration:", exam_duration)  # Debug print

            form.instance.exam_duration = exam_duration
            new_exam = form.save(commit=False)
            new_exam.section = section
            if new_exam.exam_time:
                new_exam.exam_time = timezone.make_aware(new_exam.exam_time, timezone.get_current_timezone())
            new_exam.save()

            messages.success(request, "Class added successfully")
            return redirect('custom_dashboard')
        else:
            print("Form errors:", form.errors)  # Check the form errors if they occur
    else:
        form = ExamCreateForm()  # Initialize the form

    return render(request, 'custom_admin/add_exam.html', {'form': form, 'assigned_section': section})

@login_required
def delete_exam(request, exam_id):
    exam_obj = get_object_or_404(Exams, id=exam_id)

    if request.user == exam_obj.section.class_representative:
        exam_obj.delete()
        messages.success(request, "Class deleted succesfully")
    else:
        messages.error(request, "You don't have permission to delete the class.")
    
    return redirect('custom_dashboard')

@login_required
def update_exam(request, exam_id):
    exam_obj = get_object_or_404(Exams, id=exam_id)
    assigned_section = Section.objects.filter(class_representative=request.user).first()

    if request.method == "POST":
        form = ExamUpdateForm(request.POST, instance=exam_obj)
        if form.is_valid():
            exam_obj = form.save(commit=False)
            hours = form.cleaned_data.get("hours", 0) or 0
            minutes = form.cleaned_data.get("minutes", 0) or 0
            exam_time = form.cleaned_data.get("exam_time")
            if exam_time:
                exam_obj.exam_time = exam_time.replace(second = 0)

            if hours == 0 and minutes == 0:
                messages.error(request, "Exam duration cannot be zero")
            else:
                exam_obj.duration = timedelta(hours = hours, minutes = minutes)
                exam_obj.save()
                return redirect('custom_dashboard')
        else:
            print("Form errors:", form.errors)

    else:
        form = ExamUpdateForm(instance=exam_obj)
    return render(request, 'custom_admin/change_exam.html', {
        'form': form,
        'exam_obj': exam_obj,
        'assigned_section': assigned_section,
    })

@login_required
def add_class(request):
    user = request.user

    section = Section.objects.filter(class_representative = user).first()
    if not section:
        return redirect('custom_dashboard')
    
    if request.method == "POST":
        form = ClassCreateForm(request.POST, user = user)
        if form.is_valid():
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

    # Convert to timedelta
            class_duration = timedelta(hours=hours, minutes=minutes)
    
            print("Class Duration:", class_duration)  # Debug print
    
            form.instance.class_duration = class_duration

            new_class = form.save(commit=False)
            new_class.section = section
            if new_class.start_time:
                new_class.start_time = timezone.make_aware(new_class.start_time, timezone.get_current_timezone())
            new_class.save()
            messages.success(request, "Class addes dsdbgkj")
            return redirect('custom_dashboard')
        else:
            print("Form", form.errors)
    else:
        form = ClassCreateForm(user = user)
    return render(request, 'custom_admin/add_class.html', {'form':form, 'section':section})

@login_required
def update_class(request, class_id):
    class_obj = get_object_or_404(Classes, id=class_id)

    assigned_section = None
    try:
        assigned_section=Section.objects.get(class_representative = request.user)
    except Section.DoesNotExist:
        assigned_section = None
    if request.method == "POST":
        form = ClassUpdateForm(request.POST, instance=class_obj, user=request.user)

        if form.is_valid():
            print("Form is valid")
            class_obj = form.save(commit=False)

            # Ensure start_time does not have seconds
            start_time = form.cleaned_data.get("start_time")
            if start_time:
                class_obj.start_time = start_time.replace(second=0)

            # Convert hours & minutes to duration
            hours = form.cleaned_data.get("hours", 0) or 0
            minutes = form.cleaned_data.get("minutes", 0) or 0
            if hours == 0 and minutes == 0:
                messages.error(request, "Class duration cannot be zero.")
            else:
                class_obj.class_duration = timedelta(hours=hours, minutes=minutes)

                class_obj.save()
                messages.success(request, "Class Updated Successfully")
                return redirect('custom_dashboard')

        else:
            print("Form errors", form.errors)

    else:
        form = ClassUpdateForm(instance=class_obj, user=request.user)

    return render(request, 'custom_admin/change.html', {'form': form, 'class_obj': class_obj, 'assigned_section': assigned_section})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('custom_dashboard')
        else:
            return render(request, 'custom_admin/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'custom_admin/login.html')

@login_required
def dashboard(request):

    if request.user.is_superuser:
        classes = Classes.objects.all()
        exams = Exams.objects.all()
        notices = Notices.objects.all()

    else:
        section = Section.objects.filter(class_representative = request.user).first()
        if section:
            classes = Classes.objects.filter(section=section)
            exams = Exams.objects.filter(section=section)
            notices = Notices.objects.filter(section=section)
            for ex in exams:
                ex.exam_date = ex.exam_date.strftime("%d %b")
        else:
            classes, exams, notices = [], [], []
    
    return render(request, 'custom_admin/dashboard.html', {
        'classes': classes,
        'exams': exams,
        'notices': notices,
    })


def custom_logout(request):
    logout(request)
    return redirect('custom_login')

@login_required
def delete_class(request, class_id):
    class_obj = get_object_or_404(Classes, id=class_id)

    if request.user == class_obj.section.class_representative:
        class_obj.delete()
        messages.success(request, "Class deleted succesfully")
    else:
        messages.error(request, "You don't have permission to delete the class.")
    
    return redirect('custom_dashboard')
