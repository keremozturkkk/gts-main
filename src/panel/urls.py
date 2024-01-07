from django.urls import path
from django.conf.urls import handler404, handler403

from . import views

app_name = "panel"

urlpatterns = [
    path('', views.panel_home_view, name='home'),
    path('theses/all/', views.panel_home_view, name='all_theses'),
    path('theses/my/', views.panel_my_theses_view, name='my_theses'),
    path('theses/<int:thesis_id>', views.panel_thesis_detail_view, name="thesis_detail"),
    path('theses/new/', views.panel_new_thesis_view, name="new_thesis"),
    path('theses/<int:thesis_id>/edit/', views.panel_edit_thesis_view, name="edit_thesis"),
    
    path('universities/all/', views.panel_all_universities_view, name='all_universities'),
    path('universities/<int:university_id>', views.panel_university_detail_view, name='university_detail'),
    path('universities/new/', views.panel_new_university_view, name='new_university'),
    path('universities/<int:university_id>/edit/', views.panel_edit_university_view, name='edit_university'),
    
    path('institutes/all/', views.panel_all_institutes_view, name='all_institutes'),
    path('institutes/<int:institute_id>', views.panel_institute_detail_view, name='institute_detail'),
    path('institutes/new/', views.panel_new_institute_view, name='new_institute'),
    path('institutes/<int:institute_id>/edit/', views.panel_edit_institute_view, name='edit_institute'),
    
    
    #path('types/all/', views.panel_all_types_view, name='all_types'),
    #path('types/<int:type_id>', views.panel_type_detail_view, name='type_detail'),
    #path('types/new/', views.panel_new_type_view, name='new_type'),
    #path('types/<int:type_id>/edit/', views.panel_edit_type_view, name='edit_type'),
    
    path('languages/all/', views.panel_all_languages_view, name='all_languages'),
    path('languages/<int:language_id>', views.panel_language_detail_view, name='language_detail'),
    path('languages/new/', views.panel_new_language_view, name='new_language'),
    path('languages/<int:language_id>/edit/', views.panel_edit_language_view, name='edit_language'),

]

handler404 = views.panel_404_view