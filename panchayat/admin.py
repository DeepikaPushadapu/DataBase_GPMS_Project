from django.contrib import admin
from django.db import connection

def execute_query(query, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

class RawSQLModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return execute_query(self.raw_query)

    def get_object(self, request, object_id):
        query = f"{self.raw_query} WHERE {self.pk_field} = %s"
        result = execute_query(query, [object_id])
        return result[0] if result else None

# @admin.register(Citizen)
# class CitizenAdmin(RawSQLModelAdmin):
#     list_display = ('citizen_id', 'name', 'gender', 'dob', 'household_id', 'educational_qualification', 'phone_number')
#     search_fields = ('name', 'citizen_id')
#     raw_query = "SELECT * FROM panchayat_citizen"
#     pk_field = 'citizen_id'

# @admin.register(PanchayatEmployee)
# class PanchayatEmployeeAdmin(RawSQLModelAdmin):
#     list_display = ('employee_id', 'citizen_id', 'role')
#     search_fields = ('role', 'employee_id')
#     raw_query = "SELECT * FROM panchayat_panchayatemployee"
#     pk_field = 'employee_id'

# @admin.register(GovernmentMonitor)
# class GovernmentMonitorAdmin(RawSQLModelAdmin):
#     list_display = ('monitor_id', 'citizen_id', 'role')
#     search_fields = ('role', 'monitor_id')
#     raw_query = "SELECT * FROM panchayat_governmentmonitor"
#     pk_field = 'monitor_id'

# @admin.register(Household)
# class HouseholdAdmin(RawSQLModelAdmin):
#     list_display = ('household_id', 'address', 'income')
#     search_fields = ('address', 'household_id')
#     raw_query = "SELECT * FROM panchayat_household"
#     pk_field = 'household_id'
