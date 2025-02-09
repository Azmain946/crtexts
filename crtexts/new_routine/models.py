from django.db import models
import datetime
from django.contrib.auth.models import User

class Institute(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Dept(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    department = models.CharField(max_length=30)

    def __str__(self):
        return self.department

class Batch(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    department = models.ForeignKey(Dept, on_delete=models.CASCADE)
    batch = models.CharField(max_length=25)

    def __str__(self):
        return self.batch

class Section(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    department = models.ForeignKey(Dept, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    section = models.CharField(max_length=30)
    class_representative = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.batch} - {self.section}"

# Class Representative assigned to a single section
class ClassRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.OneToOneField(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"CR: {self.user.username} - {self.section}"

class Days(models.Model):
    name = models.CharField(max_length=10, unique=True)  # e.g., "Saturday", "Sunday"

    def __str__(self):
        return self.name  # Display the name in Django Admin

# Classes are now specific to a section
class Classes(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="classes")  
    day = models.ForeignKey(Days, on_delete=models.CASCADE, related_name="classes")  
    start_time = models.TimeField()
    class_duration = models.DurationField()
    course_name = models.CharField(max_length=50)
    course_teacher = models.CharField(max_length=30)
    paused = models.BooleanField(default=False, blank=True, null=True)

    @property
    def end_time(self):
        """Calculate class end time"""
        return (datetime.datetime.combine(datetime.date.today(), self.start_time) + self.class_duration).time()

    def __str__(self):
        return f"{self.course_name} ({self.day} {self.start_time} - {self.end_time}) - {self.section}"

# Notices are now linked to a section
class Notices(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="notices")  
    notice_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)
    notice = models.TextField()

    def __str__(self):
        return f"Notice: {self.title} ({self.notice_date.date()}) - {self.section}"

# Exams are now linked to a section
class Exams(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="exams")  
    exam_name = models.CharField(max_length=50)
    duration = models.DurationField(blank=True, null=True)
    exam_date = models.DateTimeField()
    exam_time = models.TimeField(blank=True, null=True)
    syllabus = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.exam_name} on {self.exam_date.date()} - {self.section}"

# Routine specific to each section
class Routine(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name="routine")
    details = models.TextField()  # Store routine details as JSON or HTML table

    def __str__(self):
        return f"Routine for {self.section}"
