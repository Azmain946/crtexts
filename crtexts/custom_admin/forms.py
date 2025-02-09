from django import forms
from new_routine.models import *
from datetime import timedelta, time

class CreateNoticeForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['title', 'notice']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def clean(self):
        return super().clean()
    
class UpdateNoticeForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['title', 'notice',]
        # Again, 'notice_date' is not included in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #self.fields['section'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic can be added here
        return cleaned_data

       


class ClassCreateForm(forms.ModelForm):
    hours = forms.IntegerField(label="Hours", min_value=0, required=False, initial=0)
    minutes = forms.IntegerField(label="Minutes", min_value=0, max_value=59, required=False, initial=0)

    class Meta:
        model = Classes
        fields = ['day', 'start_time', 'course_name', 'course_teacher']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)

        # If user exists, filter the section to only the assigned section
        if self.user:
            #self.fields['section'].queryset = Section.objects.filter(class_representative=self.user)
            pass

        self.fields['hours'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hours'})
        self.fields['minutes'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Minutes'})

    def clean(self):
        cleaned_data = super().clean()

        # Get hours and minutes from cleaned_data
        hours = cleaned_data.get('hours', 0) or 0
        minutes = cleaned_data.get('minutes', 0) or 0

        # Ensure class_duration is set properly
        if hours == 0 and minutes == 0:
            self.add_error('minutes', "Class duration cannot be zero.")

        cleaned_data['class_duration'] = timedelta(hours=hours, minutes=minutes)

        # Ensure start_time does not have seconds
        start_time = cleaned_data.get('start_time')
        if start_time:
            cleaned_data['start_time'] = time(start_time.hour, start_time.minute, 0)

        return cleaned_data
    
class ExamCreateForm(forms.ModelForm):
    hours = forms.IntegerField(label="Hours", min_value=0, required=True, initial=0)
    minutes = forms.IntegerField(label="Minutes", min_value=0, max_value=59, required=True, initial=0)

    class Meta:
        model = Exams
        fields = ['exam_name', 'duration', 'exam_time', 'exam_date', 'syllabus']
        widgets = {
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Handle user here if needed
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours', 0)
        minutes = cleaned_data.get('minutes', 0)

        if hours == 0 and minutes == 0:
            self.add_error('Exam duration cannot be zero')

        cleaned_data['duration'] = timedelta(hours=hours, minutes=minutes, seconds=0)

        exam_time = cleaned_data.get('exam_time')
        if exam_time:
            cleaned_data['exam_time'] = time(exam_time.hour, exam_time.minute, 0)

        return cleaned_data

    
class ExamUpdateForm(forms.ModelForm):
    hours = forms.IntegerField(label="Hours", min_value=0, required=False, initial=0)
    minutes = forms.IntegerField(label="Minutes", min_value=0, max_value=59, required=False, initial=0)
    class Meta:
        model = Exams
        fields = ['exam_name', 'duration','exam_time', 'exam_date', 'syllabus']
        widgets = {
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours', 0) or 0
        minutes = cleaned_data.get('minutes', 0) or 0

        if hours == 0 and minutes == 0:
            self.add_error('Exam duration cannot be zero')
        
        cleaned_data['duration'] = timedelta(hours=hours, minutes=minutes, seconds=0)

        exam_time = cleaned_data.get('exam_time')
        if exam_time:
            cleaned_data['exam_time'] = time(exam_time.hour, exam_time.minute, 0)

        return cleaned_data
        


class ClassUpdateForm(forms.ModelForm):
    hours = forms.IntegerField(label="Hours", min_value=0, required=False, initial=0)
    minutes = forms.IntegerField(label="Minutes", min_value=0, max_value=59, required=False, initial=0)

    class Meta:
        model = Classes
        fields = [ 'day', 'start_time', 'course_name', 'course_teacher']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Start Time', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user passed in kwargs
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            cr_section = ClassRepresentative.objects.filter(user=user).first()
            
                

        self.fields['hours'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hours'})
        self.fields['minutes'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Minutes'})

    def clean(self):
        cleaned_data = super().clean()

        # Get hours and minutes from cleaned_data
        hours = cleaned_data.get('hours', 0) or 0
        minutes = cleaned_data.get('minutes', 0) or 0

        # Ensure class_duration is set properly
        if hours == 0 and minutes == 0:
            self.add_error('minutes', "Class duration cannot be zero.")

        cleaned_data['class_duration'] = timedelta(hours=hours, minutes=minutes)

        # Ensure start_time does not have seconds
        start_time = cleaned_data.get('start_time')
        if start_time:
            cleaned_data['start_time'] = time(start_time.hour, start_time.minute, 0)

        return cleaned_data
