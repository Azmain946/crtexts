from django.contrib import admin
from .models import Days, Classes, Notices, Exams, Institute, Dept, Batch, Section

admin.site.register(Institute)
admin.site.register(Dept)
admin.site.register(Batch)
admin.site.register(Section)

@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BaseCRAdmin(admin.ModelAdmin):
    """Base admin class to restrict CRs to only their section's data"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see everything
        return qs.filter(section__class_representative=request.user)  # CRs only see their section

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "section":
            if request.user.is_superuser:
                kwargs["queryset"] = Section.objects.all()  # Superusers see all sections
            else:
                kwargs["queryset"] = Section.objects.filter(class_representative=request.user)  # CR sees only their section
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Classes)
class ClassesAdmin(BaseCRAdmin):
    list_display = ('course_name', 'day', 'start_time', 'end_time', 'course_teacher', 'paused')

@admin.register(Exams)
class ExamsAdmin(BaseCRAdmin):
    list_display = ('exam_name', 'exam_date', 'duration')

@admin.register(Notices)
class NoticesAdmin(BaseCRAdmin):
    list_display = ('notice_date', 'section', 'title')
