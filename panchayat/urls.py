from django.urls import path
from . import views

urlpatterns = [
    path('citizen_dashboard/<int:citizen_id>/', views.citizen_dashboard, name='citizen_dashboard'),
    path('employee_dashboard/<int:employee_id>/', views.employee_dashboard, name='employee_dashboard'),
    path('profile/<int:citizen_id>/', views.citizen_profile, name='citizen_profile'),
    path('employee_list/', views.employee_list, name='employee_list'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('custom_admin_dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('view_table_data/<str:table_name>/', views.view_table_data, name='view_table_data'),
    path('modify_table_data/<str:table_name>/', views.modify_table_data, name='modify_table_data'),

    path('citizen/<int:citizen_id>/land_records/', views.citizen_landrecords, name='citizen_landrecords'),
    path('citizen/<int:citizen_id>/tax_records/', views.citizen_tax_records, name='citizen_tax_records'),
    path('citizen/<int:citizen_id>/welfare_schemes/', views.citizen_welfare_schemes, name='citizen_welfare_schemes'),
    path('citizen/<int:citizen_id>/complaints/', views.citizen_complaints, name='citizen_complaints'),
    path('citizen/<int:citizen_id>/add_complaint/', views.add_complaint, name='add_complaint'),

    path('employee/<int:employee_id>/profile/', views.employee_profile, name='employee_profile'),
    path('employee/<int:employee_id>/citizen_management/', views.employee_citizen_management, name='employee_citizen_management'),
    path('employee/<int:employee_id>/citizen_edit/<int:citizen_id>/', views.employee_citizen_edit, name='employee_citizen_edit'),

    path('employee/<int:employee_id>/household_management/', views.employee_household_management, name='employee_household_management'),
    path('employee/<int:employee_id>/household_edit/<int:household_id>/', views.employee_household_edit, name='employee_household_edit'),

    path('employee/<int:employee_id>/land_records_management/', views.employee_land_records_management, name='employee_land_records_management'),
    path('employee/<int:employee_id>/land_records_edit/<int:land_id>/', views.employee_land_records_edit, name='employee_land_records_edit'),

    path('employee/<int:employee_id>/welfare_scheme_management/', views.employee_welfare_scheme_management, name='employee_welfare_scheme_management'),
    path('employee/<int:employee_id>/deroll_citizen/<int:enrollment_id>/', views.employee_deroll_citizen, name='employee_deroll_citizen'),
    path('employee/<int:employee_id>/enroll_citizen/', views.employee_enroll_citizen, name='employee_enroll_citizen'),

    path('employee/<int:employee_id>/asset_management/', views.employee_asset_management, name='employee_asset_management'),
    path('employee/<int:employee_id>/asset_edit/<int:asset_id>/', views.employee_asset_edit, name='employee_asset_edit'),

    path('employee/<int:employee_id>/complaint_management/', views.employee_complaint_management, name='employee_complaint_management'),
    path('employee/<int:employee_id>/complaint_edit/<int:complaint_id>/', views.employee_complaint_edit, name='employee_complaint_edit'),

    path('employee/<int:employee_id>/tax_management/', views.employee_tax_management, name='employee_tax_management'),
    path('employee/<int:employee_id>/tax_edit/<int:tax_id>/', views.employee_tax_edit, name='employee_tax_edit'),

    path('employee/<int:employee_id>/expenditure_management/', views.employee_expenditure_management, name='employee_expenditure_management'),
    path('employee/<int:employee_id>/expenditure_edit/<int:expenditure_id>/', views.employee_expenditure_edit, name='employee_expenditure_edit'),

    path('monitor_dashboard/<int:monitor_id>/', views.monitor_dashboard, name='monitor_dashboard'),
    path('monitor_schemes/<int:monitor_id>/', views.monitor_schemes, name='monitor_schemes'),
    path('monitor/<int:monitor_id>/profile/', views.monitor_profile, name='monitor_profile'),

    path('monitor_scheme_details/<int:monitor_id>/<int:scheme_id>/', views.monitor_scheme_details, name='monitor_scheme_details'),
    
    path('monitor_population/<int:monitor_id>/', views.monitor_population, name='monitor_population'),
    path('monitor_population/<int:monitor_id>/male/', views.monitor_population_male, name='monitor_population_male'),
    path('monitor_population/<int:monitor_id>/female/', views.monitor_population_female, name='monitor_population_female'),
    path('monitor_population/<int:monitor_id>/children/', views.monitor_population_children, name='monitor_population_children'),
    path('monitor_population/<int:monitor_id>/adults/', views.monitor_population_adults, name='monitor_population_adults'),
    path('monitor_population/<int:monitor_id>/elderly/', views.monitor_population_elderly, name='monitor_population_elderly'),

    path('monitor_households/<int:monitor_id>/', views.monitor_households, name='monitor_households'),
    path('monitor_household_details/<int:monitor_id>/<int:household_id>/', views.monitor_household_details, name='monitor_household_details'),

    path('monitor_landrecords/<int:monitor_id>/', views.monitor_landrecords, name='monitor_landrecords'),
    path('monitor_agriculture/<int:monitor_id>/', views.monitor_agriculture, name='monitor_agriculture'),
    path('monitor_expenditure/<int:monitor_id>/', views.monitor_expenditure, name='monitor_expenditure'),
    path('monitor_complaints/<int:monitor_id>/', views.monitor_complaints, name='monitor_complaints'),
    path('monitor_assets/<int:monitor_id>/', views.monitor_assets, name='monitor_assets'),
]
