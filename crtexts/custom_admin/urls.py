from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name="custom_login"),
    path('dashboard/', views.dashboard, name = 'custom_dashboard'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/classes/change/<int:class_id>', views.update_class, name='update_class'),
    path('dashboard/classes/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('dashboard/exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('dashboard/classes/add/', views.add_class, name='add_class'),
    path('dashboard/exams/add/', views.add_exam, name='add_exam'),
    path('dashboard/exams/change/<int:exam_id>', views.update_exam, name='update_exam'),
    path('dashboard/notices/add/', views.add_notice, name='add_notice'),
    path('dashboard/notices/change/<int:notice_id>', views.update_notice, name='update_notice'),
    path('dashboard/notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('dashboard/pause/class/<int:class_id>', views.cancel_class, name='cancel_class')

]
