from django.shortcuts import render, redirect,get_object_or_404
from django.db import connection
from django.contrib import messages
from django.db import OperationalError, DatabaseError
import logging
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.db import transaction
import psycopg2
import time
from django.db import connection, OperationalError, DatabaseError


logger = logging.getLogger(__name__)
def execute_query(query, params=None):
    try:
        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if query.strip().upper().startswith('SELECT') or 'RETURNING' in query.upper():
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                return cursor.rowcount
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        # Handle the error (e.g., retry logic, fallback behavior)
        raise
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        # Handle other database-related errors
        raise



# def login_view(request):
    # if request.method == 'POST':
    #     user_id = request.POST['user']
    #     password = request.POST['pass']
    #     role = request.POST['role']

    #     print(f"User ID: {user_id}, Role: {role}")  # Debugging statement

    #     if role == 'citizen':
    #         query = "SELECT * FROM citizens WHERE citizen_id = %s"
    #         result = execute_query(query, [user_id])
    #         if result and result[0]['password'] == password:
    #             print("Citizen login successful")
    #             return citizen_dashboard(request, user_id)
    #         else:
    #             print("Invalid credentials for citizen")
    #             return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

    #     elif role == 'employee':
    #         query = "SELECT * FROM panchayat_employees WHERE employee_id = %s"
    #         result = execute_query(query, [user_id])
    #         if result and result[0]['password'] == password:
    #             print("Employee login successful")
    #             return employee_dashboard(request, user_id)
    #         else:
    #             print("Invalid credentials for employee")
    #             return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

    #     elif role == 'government_monitor':
    #         query = "SELECT * FROM govt_monitor WHERE monitor_id = %s"
    #         result = execute_query(query, [user_id])
    #         if result and result[0]['password'] == password:
    #             print("Government monitor login successful")
    #             return monitor_dashboard(request, user_id)
    #         else:
    #             print("Invalid credentials for government monitor")
    #             return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

    #     else:
    #         print("Invalid role")
    #         return render(request, 'panchayat/main_page.html', {'error': 'Invalid role'})

    # return render(request, 'panchayat/main_page.html')
def login_view(request):
    if request.method == 'POST':
        user_id = request.POST['user']
        password = request.POST['pass']
        role = request.POST['role']

        print(f"User ID: {user_id}, Role: {role}")  # Debugging statement

        if role == 'admin':
            if user_id == 'admin' and password == 'password':
                return redirect('custom_admin_dashboard')
            else:
                print("Invalid credentials for admin")
                return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

        elif role == 'citizen':
            query = "SELECT * FROM citizens WHERE citizen_id = %s"
            result = execute_query(query, [user_id])
            if result and result[0]['password'] == password:
                print("Citizen login successful")
                return citizen_dashboard(request, user_id)
            else:
                print("Invalid credentials for citizen")
                return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

        elif role == 'employee':
            query = "SELECT * FROM panchayat_employees WHERE employee_id = %s"
            result = execute_query(query, [user_id])
            if result and result[0]['password'] == password:
                print("Employee login successful")
                return employee_dashboard(request, user_id)
            else:
                print("Invalid credentials for employee")
                return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

        elif role == 'government_monitor':
            query = "SELECT * FROM govt_monitor WHERE monitor_id = %s"
            result = execute_query(query, [user_id])
            if result and result[0]['password'] == password:
                print("Government monitor login successful")
                return monitor_dashboard(request, user_id)
            else:
                print("Invalid credentials for government monitor")
                return render(request, 'panchayat/main_page.html', {'error': 'Invalid credentials'})

        else:
            print("Invalid role")
            return render(request, 'panchayat/main_page.html', {'error': 'Invalid role'})

    return render(request, 'panchayat/main_page.html')


def forgot_password(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        id = request.POST.get('id')
        dob = request.POST.get('dob')

        query = ""
        if role == 'citizen':
            query = "SELECT * FROM citizens WHERE citizen_id = %s AND dob = %s"
        elif role == 'government_monitor':
            query = "SELECT * FROM govt_monitor WHERE monitor_id = %s AND dob = %s"
        elif role == 'panchayat_employee':
            query = "SELECT * FROM panchayat_employees WHERE employee_id = %s AND dob = %s"
        
        with connection.cursor() as cursor:
            cursor.execute(query, [id, dob])
            user = cursor.fetchone()

        if user:
            request.session['reset_user_id'] = id
            request.session['reset_user_role'] = role
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user_id = request.session.get('reset_user_id')
            user_role = request.session.get('reset_user_role')

            query = ""
            if user_role == 'citizen':
                query = "UPDATE citizens SET password = %s WHERE citizen_id = %s"
            elif user_role == 'government_monitor':
                query = "UPDATE govt_monitor SET password = %s WHERE monitor_id = %s"
            elif user_role == 'panchayat_employee':
                query = "UPDATE panchayat_employees SET password = %s WHERE employee_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(query, [new_password, user_id])
                connection.commit()

            messages.success(request, 'Password updated successfully')
            print(list(messages.get_messages(request))) 
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'reset_password.html')


def custom_admin_dashboard(request):
    tables_query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN (
        'households', 'citizens', 'land_records', 'panchayat_employees', 
        'govt_monitor', 'assets', 'welfare_schemes', 'scheme_enrollments', 
        'tax', 'complaints', 'budget', 'panchayat_expenditure'
    )
    ORDER BY table_name
    """

    # tables_query = """
    # SELECT table_name 
    # FROM information_schema.tables 
    # WHERE table_schema = 'public'
    # """
    tables = execute_query(tables_query)
    context = {
        'tables': tables,
    }
    return render(request, 'panchayat/custom_admin_dashboard.html', context)


def view_table_data(request, table_name):
    search_query = request.GET.get('search', '')
    
    if search_query:
        query = f"""
            SELECT * FROM {table_name}
            WHERE CAST(row_to_json({table_name}) AS TEXT) ILIKE %s
        """
        data = execute_query(query, [f'%{search_query}%'])
    else:
        query = f"SELECT * FROM {table_name}"
        data = execute_query(query)

    context = {
        'table_name': table_name,
        'data': data,
        'search_query': search_query
    }
    return render(request, 'panchayat/view_table_data.html', context)


def get_table_columns(table_name):
    query = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = %s
    """
    columns = [col['column_name'] for col in execute_query(query, [table_name])]
    return columns


def modify_table_data(request, table_name):
    search_query = request.GET.get('search', '')
    columns = get_table_columns(table_name)
    primary_key_column = get_primary_key_column(table_name)

    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            with transaction.atomic():
                if action == 'add':
                    handle_add(request, table_name, columns)
                elif action == 'update':
                    handle_update(request, table_name, columns, primary_key_column)
                elif action == 'delete':
                    handle_delete(request, table_name, primary_key_column)
            return redirect('modify_table_data', table_name=table_name)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    if search_query:
        query = f"SELECT * FROM {table_name} WHERE CAST(row_to_json({table_name}) AS TEXT) ILIKE %s"
        data = execute_query(query, [f'%{search_query}%'])
    else:
        query = f"SELECT * FROM {table_name}"
        data = execute_query(query)

    context = {
        'table_name': table_name,
        'data': data,
        'search_query': search_query,
        'columns': columns,
        'primary_key_column': primary_key_column,
    }
    return render(request, 'panchayat/modify_table_data.html', context)


def handle_add(request, table_name, columns):
    new_row_data = {k: v for k, v in request.POST.items() if k in columns}
    columns_str = ', '.join(new_row_data.keys())
    values = ', '.join(['%s'] * len(new_row_data))
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values})"
    execute_query(query, list(new_row_data.values()))
    messages.success(request, "New row added successfully.")


def get_primary_key_column(table_name):
    query = f"""
    SELECT column_name
    FROM information_schema.key_column_usage
    WHERE table_name = %s
    AND constraint_name = %s
    """
    constraint_name = f'{table_name}_pkey'  # Naming convention for primary key constraints
    result = execute_query(query, [table_name, constraint_name])
    if result:
        return result[0]['column_name']
    return 'id'  # Default to 'id' if primary key is not found

 
def handle_update(request, table_name, columns, primary_key_column):
    row_id = request.POST.get('id')  # Get the primary key from the form
    update_data = {k: v for k, v in request.POST.items() if k in columns and k != 'id'}  # Exclude 'id'

    # Handle date formatting if necessary
    for key, value in update_data.items():
        if isinstance(value, str):
            try:
                update_data[key] = datetime.strptime(value, '%b. %d, %Y').strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD
            except ValueError:
                pass  # If it's not a date, leave it as is

    # Construct the SET clause for the update query
    set_clause = ', '.join([f"{k} = %s" for k in update_data.keys()])
    
    # Construct the update query
    query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_column} = %s"
    
    # Prepare the values for the query
    values = list(update_data.values()) + [row_id]

    try:
        execute_query(query, values)
        messages.success(request, "Row updated successfully.")
    except Exception as e:
        messages.error(request, f"Update failed: {e}")

    return redirect('modify_table_data', table_name=table_name)  # Redirect to reload the page


def handle_delete(request, table_name, primary_key_column):
    row_id = request.POST.get('id')
    
    try:
        with transaction.atomic():
            query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
            execute_query(query, [row_id])
        messages.success(request, f"Row and related data deleted successfully from {table_name}.")
    except Exception as e:
        messages.error(request, f"Error deleting row: {str(e)}")

    return redirect('modify_table_data', table_name=table_name)



def citizen_dashboard(request, citizen_id):

    citizen_query = "SELECT * FROM citizens WHERE citizen_id = %s"

    result = execute_query(citizen_query, [citizen_id])

    if result:

        citizen = result[0]

        return render(request, 'panchayat/citizen_dashboard.html', {'citizen': citizen})

    else:

        return render(request, 'panchayat/error.html', {'error': 'Citizen not found'})


def citizen_profile(request, citizen_id):
    query = "SELECT * FROM citizens WHERE citizen_id = %s"
    result = execute_query(query, [citizen_id])
    if result:
        citizen = result[0]
        return render(request, 'panchayat/citizen_profile.html', {'citizen': citizen})
    else:
        return render(request, 'panchayat/error.html', {'error': 'Citizen not found'})
    

def citizen_landrecords(request, citizen_id):
    # Fetch citizen details
    citizen_query = "SELECT * FROM citizens WHERE citizen_id = %s"
    citizen_result = execute_query(citizen_query, [citizen_id])
    
    if not citizen_result:
        return render(request, 'error.html', {'message': 'Citizen not found'})
    
    citizen = citizen_result[0]
    
    # Fetch land records for the citizen
    land_records_query = """
    SELECT * FROM land_records 
    WHERE citizen_id = %s
    """
    land_records = execute_query(land_records_query, [citizen_id])
    
    context = {
        'citizen': citizen,
        'land_records': land_records
    }
    
    return render(request, 'panchayat/citizen_landrecords.html', context)

def employee_list(request):
    query = """
    SELECT pe.employee_id, pe.role, c.name, c.phone_number, c.gender
    FROM panchayat_employees pe
    JOIN citizens c ON pe.citizen_id = c.citizen_id
    """
    employees = execute_query(query)
    return render(request, 'panchayat/employee_list.html', {'employees': employees})

def citizen_tax_records(request, citizen_id):
    # Fetch citizen details
    citizen_query = "SELECT * FROM citizens WHERE citizen_id = %s"
    citizen_result = execute_query(citizen_query, [citizen_id])
    
    if not citizen_result:
        return render(request, 'error.html', {'message': 'Citizen not found'})
    
    citizen = citizen_result[0]
    
    # Fetch tax records for the citizen
    tax_records_query = """
    SELECT * FROM tax 
    WHERE citizen_id = %s
    ORDER BY due_date DESC
    """
    tax_records = execute_query(tax_records_query, [citizen_id])
    
    context = {
        'citizen': citizen,
        'tax_records': tax_records
    }
    
    return render(request, 'panchayat/citizen_tax.html', context)

def citizen_welfare_schemes(request, citizen_id):
    # Fetch citizen details
    citizen_query = "SELECT * FROM citizens WHERE citizen_id = %s"
    citizen_result = execute_query(citizen_query, [citizen_id])
    
    if not citizen_result:
        return render(request, 'error.html', {'message': 'Citizen not found'})
    
    citizen = citizen_result[0]
    
    # Fetch all welfare schemes
    welfare_schemes_query = "SELECT * FROM welfare_schemes"
    welfare_schemes = execute_query(welfare_schemes_query)
    
    context = {
        'citizen': citizen,
        'welfare_schemes': welfare_schemes
    }
    
    return render(request, 'panchayat/citizen_welfare_scheme.html', context)

def citizen_complaints(request, citizen_id):
    if request.method == 'POST':
        complaint_text = request.POST['complaint']
        query = """
        INSERT INTO complaints (citizen_id, complaint, status, remarks)
        VALUES (%s, %s, 'Pending', '')
        """
        execute_query(query, [citizen_id, complaint_text])
        return redirect('citizen_complaints', citizen_id=citizen_id)

    query = """
    SELECT * FROM complaints
    WHERE citizen_id = %s
    ORDER BY complaint_id DESC
    """
    complaints = execute_query(query, [citizen_id])

    context = {
        'citizen': {'citizen_id': citizen_id},
        'complaints': complaints
    }
    return render(request, 'panchayat/citizen_complaints.html', context)


def add_complaint(request, citizen_id):
    if request.method == 'POST':
        complaint_text = request.POST['complaint']
        query = """
        INSERT INTO complaints (citizen_id, complaint, status, remarks)
        VALUES (%s, %s, 'Pending', '')
        RETURNING complaint_id
        """
        result = execute_query(query, [citizen_id, complaint_text])
        if result:
            messages.success(request, 'Complaint submitted successfully.')
            return redirect('citizen_complaints', citizen_id=citizen_id)
        else:
            messages.error(request, 'Failed to submit complaint. Please try again.')
    
    return render(request, 'panchayat/add_complaint.html', {'citizen_id': citizen_id})


def employee_dashboard(request, employee_id):
    #  Fetch employee data using employee_id
    query = """
    SELECT pe.employee_id, pe.role, c.*
    FROM panchayat_employees pe
    JOIN citizens c ON pe.citizen_id = c.citizen_id
    WHERE pe.employee_id = %s
    """
    result = execute_query(query, [employee_id])

    if result:
        employee_data = result[0]
        return render(request, 'panchayat/employee_dashboard.html', {'employee': employee_data})
    else:
        # return render(request, 'panchayat/error.html', {'error': 'Employee not found'})
        return

def employee_profile(request, employee_id):
    query = """
    SELECT pe.employee_id, pe.role, c.*
    FROM panchayat_employees pe
    JOIN citizens c ON pe.citizen_id = c.citizen_id
    WHERE pe.employee_id = %s
    """
    result = execute_query(query, [employee_id])
    if result:
        employee = result[0]
        return render(request, 'panchayat/employee_profile.html', {'employee': employee})
    else:
        return render(request, 'panchayat/error.html', {'error': 'Employee not found'})


def employee_citizen_management(request, employee_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT * FROM citizens
            WHERE name ILIKE %s OR citizen_id::text ILIKE %s
            ORDER BY citizen_id ASC
        """
        citizens = execute_query(query, [f'%{search_query}%', f'%{search_query}%'])
    else:
        # Default query if no search term is provided
        query = "SELECT * FROM citizens ORDER BY citizen_id ASC"
        citizens = execute_query(query)

    return render(request, 'panchayat/employee_citizen_management.html', {
        'citizens': citizens,
        'employee_id': employee_id,
        'search_query': search_query  # Pass the search query back to the template
    })



def employee_citizen_edit(request, employee_id,citizen_id):
    # Get citizen details
    citizen_query = "SELECT * FROM citizens WHERE citizen_id = %s"
    citizen_result = execute_query(citizen_query, [citizen_id])

    if not citizen_result:
        messages.error(request, "Citizen not found.")
        return redirect('employee_citizen_management')

    citizen = citizen_result[0]

    # Get all households
    household_query = "SELECT * FROM households"
    households = execute_query(household_query)

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        educational_qualification = request.POST['educational_qualification']
        phone_number = request.POST['phone_number']
        household_id = request.POST['household_id']

        # Validate household_id is an integer
        try:
            household_id = int(household_id)
        except ValueError:
            messages.error(request, "Invalid household ID.")
            return render(request, 'panchayat/employee_citizen_edit.html', {'citizen': citizen, 'households': households})

        # *IMPORTANT*: Sanitize your inputs!  Escaping is vital for security.  Django has helpers for this.
        # See the Django documentation.  *DO NOT SKIP THIS*.

        update_query = """
            UPDATE citizens
            SET name = %s, gender = %s, dob = %s,
                educational_qualification = %s, phone_number = %s, household_id = %s
            WHERE citizen_id = %s
        """
        try:
            execute_query(update_query, [name, gender, dob, educational_qualification, phone_number, household_id, citizen_id])
            messages.success(request, "Citizen information updated successfully.")
            return redirect('employee_citizen_management',employee_id)
        except Exception as e:
            messages.error(request, f"Error updating citizen: {e}")

    # Pass the retrieved citizen and households to the template
    # return render(request, 'panchayat/employee_citizen_edit.html', {'employee_id':employee_id citizen': citizen, 'households': households})
    return render(request, 'panchayat/employee_citizen_edit.html', {'employee_id':employee_id, 'citizen': citizen, 'households': households})


#     try:
#         search_query = request.GET.get('search', '')
        
#         if search_query:
#             query = """
#                 SELECT * FROM households
#                 WHERE household_id::text ILIKE %s 
#                 OR address ILIKE %s
#                 OR income::text ILIKE %s
#                 ORDER BY household_id ASC
#             """
#             search_param = f'%{search_query}%'
#             households = execute_query(query, [search_param] * 3)
#         else:
#             query = "SELECT * FROM households ORDER BY household_id ASC"
#             households = execute_query(query)

#         return render(request, 'panchayat/employee_household_management.html', {
#             'households': households,
#             'employee_id': employee_id,
#             'search_query': search_query
#         })
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return HttpResponseServerError("An internal server error occurred.")


def employee_household_management(request, employee_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT * FROM households
            WHERE household_id::text ILIKE %s OR address ILIKE %s
            ORDER BY household_id ASC
        """
        households = execute_query(query, [f'%{search_query}%', f'%{search_query}%'])
    else:
        # Default query if no search term is provided
        query = "SELECT * FROM households ORDER BY household_id ASC"
        households = execute_query(query)

    return render(request, 'panchayat/employee_household_management.html', {
        'households': households,
        'employee_id': employee_id,
        'search_query': search_query  # Pass the search query back to the template
    })


# def employee_household_edit(request, household_id,employee_id):
#     # Get household details using raw SQL
#     household_query = "SELECT * FROM households WHERE household_id = %s"
#     household_result = execute_query(household_query, [household_id])

#     if not household_result:
#         messages.error(request, "Household not found.")
#         return redirect('employee_household_management')

#     household = household_result[0]

#     if request.method == 'POST':
#         address = request.POST['address']
#         income = request.POST['income']

#         # Validate income is a valid float
#         try:
#             income = float(income)
#         except ValueError:
#             messages.error(request, "Invalid income format.")
#             return render(request, 'panchayat/employee_household_edit.html', {'household': household,'employee_id':employee_id})

#         # Construct update query
#         update_query = """
#             UPDATE households
#             SET address = %s, income = %s
#             WHERE household_id = %s
#         """
#         try:
#             execute_query(update_query, [address, income, household_id])
#             messages.success(request, "Household information updated successfully.")
#             return redirect('employee_household_management')
#         except Exception as e:
#             messages.error(request, f"Error updating household: {e}")

#     return render(request, 'panchayat/employee_household_edit.html', {'household': household,'employee_id':employee_id})

def employee_household_edit(request, household_id, employee_id):
    # Get household details using raw SQL
    household_query = "SELECT * FROM households WHERE household_id = %s"
    household_result = execute_query(household_query, [household_id])

    if not household_result:
        messages.error(request, "Household not found.")
        return redirect('employee_household_management', employee_id=employee_id)

    household = household_result[0]

    if request.method == 'POST':
        address = request.POST['address']
        income = request.POST['income']

        # Validate income is a valid float
        try:
            income = float(income)
        except ValueError:
            messages.error(request, "Invalid income format.")
            return render(request, 'panchayat/employee_household_edit.html', {'household': household, 'employee_id': employee_id})

        # Construct update query
        update_query = """
            UPDATE households
            SET address = %s, income = %s
            WHERE household_id = %s
        """
        try:
            execute_query(update_query, [address, income, household_id])
            messages.success(request, "Household information updated successfully.")
            return redirect('employee_household_management', employee_id=employee_id)
        except Exception as e:
            messages.error(request, f"Error updating household: {e}")

    return render(request, 'panchayat/employee_household_edit.html', {'household': household, 'employee_id': employee_id})


def employee_land_records_management(request, employee_id):
    search_query = request.GET.get('search', '')

    citizens_query = "SELECT citizen_id, name FROM citizens"
    citizens = execute_query(citizens_query)

    if search_query:
        land_records_query = """
            SELECT lr.*, c.name as citizen_name
            FROM land_records lr
            JOIN citizens c ON lr.citizen_id = c.citizen_id
            WHERE lr.land_id::text ILIKE %s OR c.name ILIKE %s
            ORDER BY lr.land_id ASC
        """
        land_records = execute_query(land_records_query, [f'%{search_query}%', f'%{search_query}%'])
    else:
        land_records_query = """
            SELECT lr.*, c.name as citizen_name
            FROM land_records lr
            JOIN citizens c ON lr.citizen_id = c.citizen_id
            ORDER BY lr.land_id ASC
        """
        land_records = execute_query(land_records_query)

    if request.method == 'POST':
        citizen_id = request.POST.get('citizen_id')
        area_acres = request.POST.get('area_acres')
        crop_type = request.POST.get('crop_type')

        if not all([citizen_id, area_acres, crop_type]):
            messages.error(request, "All fields are required.")
        else:
            try:
                citizen_id = int(citizen_id)
                area_acres = float(area_acres)

                add_land_record_query = """
                    INSERT INTO land_records (citizen_id, area_acres, crop_type)
                    VALUES (%s, %s, %s)
                """
                execute_query(add_land_record_query, [citizen_id, area_acres, crop_type])

                messages.success(request, "Land record added successfully.")
                return redirect('employee_land_records_management', employee_id=employee_id)

            except ValueError:
                messages.error(request, "Invalid citizen_id or area_acres format.")
            except Exception as e:
                messages.error(request, f"Error adding land record: {e}")

    return render(request, 'panchayat/employee_land_records_management.html', {
        'land_records': land_records,
        'citizens': citizens,
        'employee_id': employee_id,
        'search_query': search_query
    })


def employee_land_records_edit(request, land_id,employee_id):
    # Get the land record to edit
    land_record_query = "SELECT * FROM land_records WHERE land_id = %s"
    land_record_result = execute_query(land_record_query, [land_id])

    if not land_record_result:
        messages.error(request, "Land record not found.")
        return redirect('employee_land_records_management')

    land_record = land_record_result[0]

    # Get all citizens
    citizens_query = "SELECT citizen_id, name FROM citizens"
    citizens = execute_query(citizens_query)

    if request.method == 'POST':
        citizen_id = request.POST['citizen_id']
        area_acres = request.POST['area_acres']
        crop_type = request.POST['crop_type']

        # Validate data
        if not all([citizen_id, area_acres, crop_type]):
            messages.error(request, "All fields are required.")
            return render(request, 'panchayat/employee_land_records_edit.html',
                          {'land_record': land_record, 'citizens': citizens})

        try:
            citizen_id = int(citizen_id)
            area_acres = float(area_acres)

            # Update the land record with raw SQL
            update_land_record_query = """
                UPDATE land_records
                SET citizen_id = %s, area_acres = %s, crop_type = %s
                WHERE land_id = %s
            """
            execute_query(update_land_record_query, [citizen_id, area_acres, crop_type, land_id])

            messages.success(request, "Land record updated successfully.")
            # return redirect('employee_land_records_management',)
            return redirect('employee_land_records_management', employee_id=employee_id)

        except ValueError:
            messages.error(request, "Invalid area_acres format.")
            return render(request, 'panchayat/employee_land_records_edit.html',
                          {'land_record': land_record, 'citizens': citizens})
        except Exception as e:
            messages.error(request, f"Error updating land record: {e}")

    return render(request, 'panchayat/employee_land_records_edit.html',
                  {'land_record': land_record, 'citizens': citizens, 'employee_id':employee_id})



def employee_welfare_scheme_management(request, employee_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    
    # Get all citizens (this is needed for the enrollment form)
    citizens_query = "SELECT citizen_id, name FROM citizens"
    available_citizens = execute_query(citizens_query)

    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT ws.*, 
                   (SELECT COUNT(*) FROM scheme_enrollments se WHERE se.scheme_id = ws.scheme_id) as enrollment_count
            FROM welfare_schemes ws
            WHERE ws.scheme_id::text ILIKE %s OR ws.name ILIKE %s
            ORDER BY ws.scheme_id ASC
        """
        welfare_schemes = execute_query(query, [f'%{search_query}%', f'%{search_query}%'])
    else:
        # Default query if no search term is provided
        query = """
            SELECT ws.*, 
                   (SELECT COUNT(*) FROM scheme_enrollments se WHERE se.scheme_id = ws.scheme_id) as enrollment_count
            FROM welfare_schemes ws
            ORDER BY ws.scheme_id ASC
        """
        welfare_schemes = execute_query(query)

    # Get enrollment data for each welfare scheme
    for scheme in welfare_schemes:
        enrollment_query = """
            SELECT se.*, c.name as citizen_name FROM scheme_enrollments se
            JOIN citizens c ON se.citizen_id = c.citizen_id
            WHERE se.scheme_id = %s
        """
        scheme['enrolled_citizens'] = execute_query(enrollment_query, [scheme['scheme_id']])

    return render(request, 'panchayat/employee_welfare_scheme_management.html', {
        'welfare_schemes': welfare_schemes,
        'available_citizens': available_citizens,
        'employee_id': employee_id,
        'search_query': search_query  # Pass the search query back to the template
    })





def employee_deroll_citizen(request, enrollment_id,employee_id):
    try:
        deroll_query = "DELETE FROM scheme_enrollments WHERE enrollment_id = %s"
        execute_query(deroll_query, [enrollment_id])
        messages.success(request, "Citizen de-enrolled successfully.")
    except Exception as e:
        messages.error(request, f"Error de-enrolling citizen: {e}")

    return redirect('employee_welfare_scheme_management',employee_id)


def employee_enroll_citizen(request,employee_id):
    if request.method == 'POST':
        scheme_id = request.POST['scheme_id']
        citizen_id = request.POST['citizen_id']
        enrollment_date = request.POST['enrollment_date']

        try:
            scheme_id = int(scheme_id)
            citizen_id = int(citizen_id)

            # Check if already enrolled
            enrollment_check_query = """
                SELECT * FROM scheme_enrollments
                WHERE citizen_id = %s AND scheme_id = %s
            """
            existing_enrollment = execute_query(enrollment_check_query, [citizen_id, scheme_id])

            if existing_enrollment:
                messages.error(request, "Citizen is already enrolled in this scheme.")
                return redirect('employee_welfare_scheme_management',employee_id)

            enrollment_query = """
                INSERT INTO scheme_enrollments (citizen_id, scheme_id, enrollment_date)
                VALUES (%s, %s, %s)
            """
            execute_query(enrollment_query, [citizen_id, scheme_id, enrollment_date])
            messages.success(request, "Citizen enrolled in scheme successfully.")

        except ValueError:
            messages.error(request, "Invalid Scheme ID or Citizen ID.")
        except Exception as e:
            messages.error(request, f"Error enrolling citizen: {e}")

    return redirect('employee_welfare_scheme_management',employee_id)

def employee_asset_management(request, employee_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    
    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT * FROM assets
            WHERE asset_id::text ILIKE %s OR type ILIKE %s OR location ILIKE %s
            ORDER BY asset_id ASC
        """
        assets = execute_query(query, [f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'])
    else:
        # Default query if no search term is provided
        query = "SELECT * FROM assets ORDER BY asset_id ASC"
        assets = execute_query(query)

    if request.method == 'POST':
        asset_type = request.POST['type']
        asset_location = request.POST['location']
        installation_date = request.POST['installation_date']
        asset_status = request.POST['status']
        asset_value = request.POST['value']

        if not all([asset_type, asset_location, installation_date, asset_status, asset_value]):
            messages.error(request, "All fields are required.")
        else:
            try:
                value = float(asset_value)
                insert_asset_query = """
                    INSERT INTO assets (type, location, installation_date, status, value)
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(insert_asset_query, [asset_type, asset_location, installation_date, asset_status, value])
                messages.success(request, "Asset added successfully.")
                return redirect('employee_asset_management', employee_id=employee_id)
            except ValueError:
                messages.error(request, "Invalid value format.")
            except Exception as e:
                messages.error(request, f"Error adding asset: {e}")

    return render(request, 'panchayat/employee_asset_management.html', {
        'assets': assets,
        'employee_id': employee_id,
        'search_query': search_query  # Pass the search query back to the template
    })



def employee_asset_edit(request, asset_id,employee_id):
    # Get the asset to edit
    asset_query = "SELECT * FROM assets WHERE asset_id = %s"
    asset_result = execute_query(asset_query, [asset_id])

    if not asset_result:
        messages.error(request, "Asset not found.")
        return redirect('employee_asset_management',employee_id)

    asset = asset_result[0]  # First object

    if request.method == 'POST':
        asset_type = request.POST['type']
        asset_location = request.POST['location']
        installation_date = request.POST['installation_date']
        asset_status = request.POST['status']
        asset_value = request.POST['value']

        try:
            value = float(asset_value)  # Convert Value

            # Update the asset
            update_asset_query = """
                UPDATE assets
                SET type = %s, location = %s, installation_date = %s, status = %s, value = %s
                WHERE asset_id = %s
            """
            execute_query(update_asset_query, [asset_type, asset_location, installation_date, asset_status, value, asset_id])
            messages.success(request, "Asset updated successfully.")
            return redirect('employee_asset_management',employee_id)

        except ValueError:
            messages.error(request, "Invalid value format.")
            return render(request, 'panchayat/employee_asset_edit.html', {'asset': asset, 'employee_id':employee_id})

        except Exception as e:
            messages.error(request, f"Error updating asset: {e}")

    return render(request, 'panchayat/employee_asset_edit.html', {'asset': asset, 'employee_id':employee_id})

def employee_complaint_management(request, employee_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters

    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT * FROM complaints
            WHERE complaint_id::text LIKE %s 
               OR LOWER(complaint) LIKE %s 
               OR LOWER(status) LIKE %s
            ORDER BY complaint_id ASC
        """
        search_param = f'%{search_query.lower()}%'
        complaints = execute_query(query, [search_param] * 3)
    else:
        # Default query if no search term is provided
        query = "SELECT * FROM complaints ORDER BY complaint_id ASC"
        complaints = execute_query(query)

    # Categorize complaints based on status
    pending_complaints = [c for c in complaints if c['status'].lower() == 'pending']
    in_progress_complaints = [c for c in complaints if c['status'].lower() == 'in progress']
    rejected_complaints = [c for c in complaints if c['status'].lower() == 'rejected']
    resolved_complaints = [c for c in complaints if c['status'].lower() == 'resolved']

    return render(request, 'panchayat/employee_complaint_management.html', {
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'rejected_complaints': rejected_complaints,
        'resolved_complaints': resolved_complaints,
        'employee_id': employee_id,
        'search_query': search_query  # Pass the search query back to the template
    })



def employee_complaint_edit(request, complaint_id,employee_id):
    # Get the complaint to edit
    complaint_query = "SELECT * FROM complaints WHERE complaint_id = %s"
    complaint_result = execute_query(complaint_query, [complaint_id])

    if not complaint_result:
        messages.error(request, "Complaint not found.")
        return redirect('employee_complaint_management',employee_id)

    complaint = complaint_result[0]

    if request.method == 'POST':
        new_status = request.POST['status']
        remarks = request.POST['remarks']

        # Update the complaint
        update_complaint_query = """
            UPDATE complaints
            SET status = %s, remarks = %s
            WHERE complaint_id = %s
        """
        try:
            execute_query(update_complaint_query, [new_status, remarks, complaint_id])
            messages.success(request, "Complaint updated successfully.")
            return redirect('employee_complaint_management',employee_id)

        except Exception as e:
            messages.error(request, f"Error updating complaint: {e}")
            return render(request, 'panchayat/employee_complaint_edit.html', {'complaint': complaint , 'employee_id':employee_id})

    return render(request, 'panchayat/employee_complaint_edit.html', {'complaint': complaint, 'employee_id':employee_id})

def employee_tax_management(request, employee_id):
    search_query = request.GET.get('search', '')

    citizens_query = "SELECT citizen_id, name FROM citizens"
    citizens = execute_query(citizens_query)

    if search_query:
        tax_records_query = """
            SELECT tax.*, c.name as citizen_name
            FROM tax
            JOIN citizens c ON tax.citizen_id = c.citizen_id
            WHERE tax.tax_id::text LIKE %s 
               OR LOWER(c.name) LIKE %s 
               OR LOWER(tax.status) LIKE %s
               OR LOWER(tax.tax_type) LIKE %s
            ORDER BY tax.tax_id ASC
        """
        search_param = f'%{search_query.lower()}%'
        tax_records = execute_query(tax_records_query, [search_param] * 4)
    else:
        tax_records_query = """
            SELECT tax.*, c.name as citizen_name
            FROM tax
            JOIN citizens c ON tax.citizen_id = c.citizen_id
            ORDER BY tax.tax_id ASC
        """
        tax_records = execute_query(tax_records_query)

    if request.method == 'POST':
        citizen_id = request.POST['citizen_id']
        amount = request.POST['amount']
        due_date = request.POST['due_date']
        status = request.POST['status']
        tax_type = request.POST['tax_type']

        if not all([citizen_id, amount, due_date, status, tax_type]):
            messages.error(request, "All fields are required.")
        else:
            try:
                citizen_id = int(citizen_id)
                amount = float(amount)

                insert_tax_query = """
                    INSERT INTO tax (citizen_id, amount, due_date, status, tax_type)
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(insert_tax_query, [citizen_id, amount, due_date, status, tax_type])
                messages.success(request, "Tax record added successfully.")
                return redirect('employee_tax_management', employee_id=employee_id)

            except ValueError:
                messages.error(request, "Invalid amount format.")
            except Exception as e:
                messages.error(request, f"Error adding tax record: {e}")

    return render(request, 'panchayat/employee_tax_management.html', {
        'tax_records': tax_records,
        'citizens': citizens,
        'employee_id': employee_id,
        'search_query': search_query
    })

def employee_tax_edit(request, tax_id, employee_id):
    tax_query = "SELECT * FROM tax WHERE tax_id = %s"
    tax_result = execute_query(tax_query, [tax_id])

    if not tax_result:
        messages.error(request, "Tax record not found.")
        return redirect('employee_tax_management', employee_id)

    tax = tax_result[0]

    citizens_query = "SELECT citizen_id, name FROM citizens"
    citizens = execute_query(citizens_query)

    if request.method == 'POST':
        citizen_id = request.POST['citizen_id']
        amount = request.POST['amount']
        due_date = request.POST['due_date']
        status = request.POST['status']
        last_paid = request.POST.get('last_paid')
        tax_type = request.POST['tax_type']

        if not all([citizen_id, amount, due_date, status, tax_type]):
            messages.error(request, "All fields are required.")
            return render(request, 'panchayat/employee_tax_edit.html',
                          {'tax': tax, 'citizens': citizens, 'employee_id': employee_id})

        try:
            citizen_id = int(citizen_id)
            amount = float(amount)

            update_tax_query = """
                UPDATE tax
                SET citizen_id = %s, amount = %s, due_date = %s, status = %s, last_paid = %s, tax_type = %s
                WHERE tax_id = %s
            """
            execute_query(update_tax_query, [citizen_id, amount, due_date, status, last_paid, tax_type, tax_id])
            messages.success(request, "Tax record updated successfully.")
            return redirect('employee_tax_management', employee_id)

        except ValueError:
            messages.error(request, "Invalid amount format.")
        except Exception as e:
            messages.error(request, f"Error updating tax record: {e}")

    return render(request, 'panchayat/employee_tax_edit.html',
                  {'tax': tax, 'citizens': citizens, 'employee_id': employee_id})


# def employee_expenditure_management(request, employee_id):
#     search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    
#     if search_query:
#         # Modify the query to filter based on the search term, including expenditure_id
#         query = """
#             SELECT * FROM budget
#             WHERE expenditure_id::text LIKE %s
#                OR type ILIKE %s 
#                OR status ILIKE %s
#             ORDER BY date DESC
#         """
#         search_param = f'%{search_query}%'
#         expenditures = execute_query(query, [search_param, search_param, search_param])
#     else:
#         # Default query if no search term is provided
#         query = "SELECT * FROM budget ORDER BY date DESC"
#         expenditures = execute_query(query)

#     if request.method == 'POST':
#         expenditure_type = request.POST['type']
#         amount = request.POST['amount']
#         date = request.POST['date']
#         status = request.POST['status']

#         if not all([expenditure_type, amount, date, status]):
#             messages.error(request, "All fields are required.")
#         else:
#             try:
#                 amount = float(amount)
#                 insert_expenditure_query = """
#                     INSERT INTO budget (type, amount, date, status)
#                     VALUES (%s, %s, %s, %s)
#                 """
#                 execute_query(insert_expenditure_query, [expenditure_type, amount, date, status])
#                 messages.success(request, "Expenditure added successfully.")
#                 return redirect('employee_expenditure_management', employee_id=employee_id)
#             except ValueError:
#                 messages.error(request, "Invalid amount format.")
#             except Exception as e:
#                 messages.error(request, f"Error adding expenditure: {e}")

#     return render(request, 'panchayat/employee_expenditure_management.html', {
#         'expenditures': expenditures,
#         'employee_id': employee_id,
#         'search_query': search_query  # Pass the search query back to the template
#     })


# def employee_expenditure_edit(request, expenditure_id,employee_id):
#     # Get the expenditure to edit
#     expenditure_query = "SELECT * FROM budget WHERE expenditure_id = %s"
#     expenditure_result = execute_query(expenditure_query, [expenditure_id])

#     if not expenditure_result:
#         messages.error(request, "Expenditure not found.")
#         return redirect('employee_expenditure_management',employee_id)

#     expenditure = expenditure_result[0]

#     if request.method == 'POST':
#         expenditure_type = request.POST['type']
#         amount = request.POST['amount']
#         date = request.POST['date']
#         status = request.POST['status']

#         # Validate data
#         if not all([expenditure_type, amount, date, status]):
#             messages.error(request, "All fields are required.")
#             return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure,'employee_id':employee_id})

#         try:
#             amount = float(amount)

#             # Update the expenditure using raw SQL
#             update_expenditure_query = """
#                 UPDATE budget
#                 SET type = %s, amount = %s, date = %s, status = %s
#                 WHERE expenditure_id = %s
#             """
#             execute_query(update_expenditure_query, [expenditure_type, amount, date, status, expenditure_id])
#             messages.success(request, "Expenditure updated successfully.")
#             return redirect('employee_expenditure_management',employee_id)

#         except ValueError:
#             messages.error(request, "Invalid amount format.")
#             return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure,'employee_id':employee_id})

#         except Exception as e:
#             messages.error(request, f"Error updating expenditure: {e}")
#             return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure,'employee_id':employee_id})

#     return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure,'employee_id':employee_id})
def employee_expenditure_management(request, employee_id):
    search_query = request.GET.get('search', '')
    
    if search_query:
        query = """
            SELECT * FROM Panchayat_Expenditure
            WHERE expenditure_id::text LIKE %s
               OR type ILIKE %s 
               OR status ILIKE %s
            ORDER BY date_of_expenditure DESC
        """
        search_param = f'%{search_query}%'
        expenditures = execute_query(query, [search_param, search_param, search_param])
    else:
        query = "SELECT * FROM Panchayat_Expenditure ORDER BY date_of_expenditure DESC"
        expenditures = execute_query(query)

    if request.method == 'POST':
        expenditure_type = request.POST['type']
        amount_spent = request.POST['amount_spent']
        date_of_expenditure = request.POST['date_of_expenditure']
        status = request.POST['status']

        if not all([expenditure_type, amount_spent, date_of_expenditure, status]):
            messages.error(request, "All fields are required.")
        else:
            try:
                amount_spent = int(amount_spent)  # Changed to int for BIGINT
                insert_expenditure_query = """
                    INSERT INTO Panchayat_Expenditure (type, amount_spent, date_of_expenditure, status)
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(insert_expenditure_query, [expenditure_type, amount_spent, date_of_expenditure, status])
                messages.success(request, "Expenditure added successfully.")
                return redirect('employee_expenditure_management', employee_id=employee_id)
            except ValueError:
                messages.error(request, "Invalid amount format.")
            except Exception as e:
                messages.error(request, f"Error adding expenditure: {e}")

    return render(request, 'panchayat/employee_expenditure_management.html', {
        'expenditures': expenditures,
        'employee_id': employee_id,
        'search_query': search_query
    })

def employee_expenditure_edit(request, expenditure_id, employee_id):
    expenditure_query = "SELECT * FROM Panchayat_Expenditure WHERE expenditure_id = %s"
    expenditure_result = execute_query(expenditure_query, [expenditure_id])

    if not expenditure_result:
        messages.error(request, "Expenditure not found.")
        return redirect('employee_expenditure_management', employee_id)

    expenditure = expenditure_result[0]

    if request.method == 'POST':
        expenditure_type = request.POST['type']
        amount_spent = request.POST['amount_spent']
        date_of_expenditure = request.POST['date_of_expenditure']
        status = request.POST['status']

        if not all([expenditure_type, amount_spent, date_of_expenditure, status]):
            messages.error(request, "All fields are required.")
            return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure, 'employee_id': employee_id})

        try:
            amount_spent = int(amount_spent)  # Changed to int for BIGINT

            update_expenditure_query = """
                UPDATE Panchayat_Expenditure
                SET type = %s, amount_spent = %s, date_of_expenditure = %s, status = %s
                WHERE expenditure_id = %s
            """
            execute_query(update_expenditure_query, [expenditure_type, amount_spent, date_of_expenditure, status, expenditure_id])
            messages.success(request, "Expenditure updated successfully.")
            return redirect('employee_expenditure_management', employee_id)

        except ValueError:
            messages.error(request, "Invalid amount format.")
        except Exception as e:
            messages.error(request, f"Error updating expenditure: {e}")

    return render(request, 'panchayat/employee_expenditure_edit.html', {'expenditure': expenditure, 'employee_id': employee_id})


def monitor_dashboard(request, monitor_id):
    # Fetch the monitor data using monitor_id
    query = """
        SELECT * FROM govt_monitor
        WHERE monitor_id = %s
    """
    result = execute_query(query, [monitor_id])
    
    if result:
        monitor = result[0]  # Get the monitor as a dictionary
        return render(request, 'panchayat/monitor_dashboard.html', {'GovernmentMonitor': monitor})
    # else:
        # return render(request, 'panchayat/error.html', {'error': 'Monitor not found'})
    else:
        print("user not found")

def monitor_profile(request, monitor_id):
    query = """
        SELECT * FROM govt_monitor
        WHERE monitor_id = %s
    """
    result = execute_query(query, [monitor_id])
    
    if result:
        monitor = result[0]  # Get the monitor as a dictionary
        return render(request, 'panchayat/monitor_profile.html', {'monitor': monitor})
    else:
        raise Http404("Monitor not found")

def monitor_schemes(request,monitor_id):
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    if search_query:
        # Modify the query to filter based on the search term
        query = """
            SELECT * FROM welfare_schemes
            WHERE scheme_id::text ILIKE %s OR name ILIKE %s OR eligibility ILIKE %s
            ORDER BY scheme_id ASC
        """
        schemes = execute_query(query, [f'%{search_query}%'] * 3)
    else:
        # Default query if no search term is provided
        query = "SELECT * FROM welfare_schemes ORDER BY scheme_id ASC"
        schemes = execute_query(query)

    return render(request, 'panchayat/monitor_schemes.html', {
        'monitor_id': monitor_id,
        'schemes': schemes,
        'search_query': search_query  # Pass the search query back to the template
    })

def monitor_scheme_details(request, scheme_id,monitor_id):
    scheme_query = """
    SELECT * FROM welfare_schemes WHERE scheme_id = %s
    """
    scheme = execute_query(scheme_query, [scheme_id])[0]

    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    if search_query:
        # Modify the query to filter based on the search term
        enrollments_query = """
        SELECT se.enrollment_id, se.enrollment_date, 
               c.citizen_id, c.name, c.gender, c.dob, c.educational_qualification
        FROM scheme_enrollments se
        JOIN citizens c ON se.citizen_id = c.citizen_id
        WHERE se.scheme_id = %s AND 
              (c.citizen_id::text ILIKE %s OR c.name ILIKE %s OR 
               c.gender ILIKE %s OR c.educational_qualification ILIKE %s)
        ORDER BY se.enrollment_id ASC
        """
        enrollments = execute_query(enrollments_query, [scheme_id] + [f'%{search_query}%'] * 4)
    else:
        # Default query if no search term is provided
        enrollments_query = """
        SELECT se.enrollment_id, se.enrollment_date, 
               c.citizen_id, c.name, c.gender, c.dob, c.educational_qualification
        FROM scheme_enrollments se
        JOIN citizens c ON se.citizen_id = c.citizen_id
        WHERE se.scheme_id = %s
        ORDER BY se.enrollment_id ASC
        """
        enrollments = execute_query(enrollments_query, [scheme_id])

    context = {
        'monitor_id': monitor_id,
        'scheme': scheme,
        'enrollments': enrollments,
        'search_query': search_query  # Pass the search query back to the template
    }
    return render(request, 'panchayat/monitor_scheme_details.html', context)

def monitor_population(request,monitor_id):
    query = """
    SELECT 
        SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) as male_count,
        SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) as female_count,
        SUM(CASE WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) < 18 THEN 1 ELSE 0 END) as children_count,
        SUM(CASE WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) BETWEEN 18 AND 60 THEN 1 ELSE 0 END) as adults_count,
        SUM(CASE WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) > 60 THEN 1 ELSE 0 END) as elderly_count
    FROM citizens
    """
    result = execute_query(query)[0]
    return render(request, 'panchayat/monitor_population.html', {**result, 'monitor_id': monitor_id})

def monitor_population_children(request,monitor_id):
    query = """
    SELECT citizen_id, name, gender, dob, EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) as age
    FROM citizens
    WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) < 18
    ORDER BY age DESC
    """
    children = execute_query(query)
    return render(request, 'panchayat/monitor_population_list.html', {'citizens': children, 'group': 'Children', 'monitor_id': monitor_id})

def monitor_population_adults(request,monitor_id):
    query = """
    SELECT citizen_id, name, gender, dob, EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) as age
    FROM citizens
    WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) BETWEEN 18 AND 60
    ORDER BY age DESC
    """
    adults = execute_query(query)
    return render(request, 'panchayat/monitor_population_list.html', {'citizens': adults, 'group': 'Adults', 'monitor_id': monitor_id})

def monitor_population_elderly(request,monitor_id):
    query = """
    SELECT citizen_id, name, gender, dob, EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) as age
    FROM citizens
    WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob)) > 60
    ORDER BY age DESC
    """
    elderly = execute_query(query)
    return render(request, 'panchayat/monitor_population_list.html', {'citizens': elderly, 'group': 'Elderly', 'monitor_id': monitor_id})


def monitor_population_male(request,monitor_id):
    query = """
    SELECT * FROM citizens WHERE gender = 'Male'
    """
    males = execute_query(query)
    return render(request, 'panchayat/monitor_population_list.html', {'citizens': males, 'gender': 'Male', 'monitor_id': monitor_id})

def monitor_population_female(request,monitor_id):
    query = """
    SELECT * FROM citizens WHERE gender = 'Female'
    """
    females = execute_query(query)
    return render(request, 'panchayat/monitor_population_list.html', {'citizens': females, 'gender': 'Female', 'monitor_id': monitor_id})


def monitor_households(request,monitor_id):
    search_id = request.GET.get('household_id', '')
    if search_id:
        query = "SELECT * FROM households WHERE household_id = %s"
        households = execute_query(query, [search_id])
    else:
        query = "SELECT * FROM households ORDER BY household_id"
        households = execute_query(query)
    return render(request, 'panchayat/monitor_households.html', {'households': households, 'monitor_id': monitor_id})

def monitor_household_details(request, household_id,monitor_id):
    household_query = "SELECT * FROM households WHERE household_id = %s"
    household = execute_query(household_query, [household_id])[0]
    
    members_query = "SELECT * FROM citizens WHERE household_id = %s"
    members = execute_query(members_query, [household_id])
    
    return render(request, 'panchayat/monitor_household_details.html', {
        'monitor_id': monitor_id,
        'household': household,
        'members': members
    })


def monitor_landrecords(request,monitor_id):
    owner_name = request.GET.get('owner_name', '')
    citizen_id = request.GET.get('citizen_id', '')
    land_id = request.GET.get('land_id', '')

    query = """
    SELECT lr.*, c.name as owner_name
    FROM land_records lr
    JOIN citizens c ON lr.citizen_id = c.citizen_id
    WHERE 1=1
    """
    params = []

    if owner_name:
        query += " AND c.name ILIKE %s"
        params.append(f'%{owner_name}%')
    if citizen_id:
        query += " AND lr.citizen_id = %s"
        params.append(citizen_id)
    if land_id:
        query += " AND lr.land_id = %s"
        params.append(land_id)

    query += " ORDER BY lr.land_id"

    land_records = execute_query(query, params)
    return render(request, 'panchayat/monitor_landrecords.html', {'land_records': land_records, 'monitor_id': monitor_id})

def monitor_agriculture(request,monitor_id):
    crop_type = request.GET.get('crop_type', '')

    query = """
    SELECT lr.land_id, lr.crop_type, c.name as owner_name
    FROM land_records lr
    JOIN citizens c ON lr.citizen_id = c.citizen_id
    """
    params = []

    if crop_type:
        query += " WHERE lr.crop_type ILIKE %s"
        params.append(f'%{crop_type}%')

    query += " ORDER BY lr.land_id"

    land_records = execute_query(query, params)

    # Calculate crop type summary
    crop_summary = {}
    for record in land_records:
        crop = record['crop_type']
        crop_summary[crop] = crop_summary.get(crop, 0) + 1

    # Prepare data for pie chart
    crop_labels = list(crop_summary.keys())
    crop_data = list(crop_summary.values())

    context = {
        'monitor_id': monitor_id,
        'land_records': land_records,
        'crop_summary': crop_summary,
        'crop_labels': crop_labels,
        'crop_data': crop_data
    }

    return render(request, 'panchayat/monitor_agriculture.html', context)


def monitor_expenditure(request, monitor_id):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    expenditure_type = request.GET.get('expenditure_type', '')
    status = request.GET.get('status', '')

    query = "SELECT * FROM Panchayat_Expenditure WHERE 1=1"
    params = []

    if start_date:
        query += " AND date_of_expenditure >= %s"
        params.append(start_date)
    if end_date:
        query += " AND date_of_expenditure <= %s"
        params.append(end_date)
    if expenditure_type:
        query += " AND type ILIKE %s"
        params.append(f"%{expenditure_type}%")
    if status:
        query += " AND status = %s"
        params.append(status)

    query += " ORDER BY date_of_expenditure DESC"

    expenditures = execute_query(query, params)

    this_year = datetime.now().year
    this_year_expenditure_query = """
    SELECT SUM(amount_spent) as total
    FROM Panchayat_Expenditure
    WHERE EXTRACT(YEAR FROM date_of_expenditure) = %s
    """
    this_year_expenditure = execute_query(this_year_expenditure_query, [this_year])[0]['total']

    chart_query = """
    SELECT EXTRACT(YEAR FROM date_of_expenditure) as year, SUM(amount_spent) as total
    FROM Panchayat_Expenditure
    GROUP BY EXTRACT(YEAR FROM date_of_expenditure)
    ORDER BY EXTRACT(YEAR FROM date_of_expenditure)
    """
    chart_data = execute_query(chart_query)

    chart_labels = [int(item['year']) for item in chart_data]
    chart_values = [float(item['total']) for item in chart_data]

    context = {
        'monitor_id': monitor_id,
        'expenditures': expenditures,
        'this_year_expenditure': this_year_expenditure,
        'chart_labels': chart_labels,
        'chart_data': chart_values,
        'start_date': start_date,
        'end_date': end_date,
        'expenditure_type': expenditure_type,
        'status': status
    }
    return render(request, 'panchayat/monitor_expenditure.html', context)

def monitor_complaints(request,monitor_id):
    citizen_id = request.GET.get('citizen_id', '')
    complaint_id = request.GET.get('complaint_id', '')
    status = request.GET.get('status', '')

    query = """
    SELECT c.complaint_id, ct.name as citizen_name, c.complaint, c.status, c.remarks
    FROM complaints c
    JOIN citizens ct ON c.citizen_id = ct.citizen_id
    WHERE 1=1
    """
    params = []

    if citizen_id:
        query += " AND c.citizen_id = %s"
        params.append(citizen_id)
    if complaint_id:
        query += " AND c.complaint_id = %s"
        params.append(complaint_id)
    if status:
        query += " AND c.status = %s"
        params.append(status)

    query += " ORDER BY c.complaint_id DESC"

    complaints = execute_query(query, params)

    context = {
        'monitor_id': monitor_id,
        'complaints': complaints,
    }
    return render(request, 'panchayat/monitor_complaints.html', context)

def monitor_assets(request,monitor_id):
    asset_id = request.GET.get('asset_id', '')
    status = request.GET.get('status', '')
    location = request.GET.get('location', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    asset_type = request.GET.get('type', '')

    query = "SELECT * FROM assets WHERE 1=1"
    params = []

    if asset_id:
        query += " AND asset_id = %s"
        params.append(asset_id)
    if status:
        query += " AND status = %s"
        params.append(status)
    if location:
        query += " AND location ILIKE %s"
        params.append(f"%{location}%")
    if from_date:
        query += " AND installation_date >= %s"
        params.append(from_date)
    if to_date:
        query += " AND installation_date <= %s"
        params.append(to_date)
    if asset_type:
        query += " AND type = %s"
        params.append(asset_type)

    query += " ORDER BY asset_id"

    assets = execute_query(query, params)

    context = {
        'monitor_id': monitor_id,
        'assets': assets,
    }
    return render(request, 'panchayat/monitor_assets.html', context)
