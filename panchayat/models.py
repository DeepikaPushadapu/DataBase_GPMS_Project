# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password 

# class Citizen(models.Model):
#     citizen_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     name = models.TextField()
#     gender = models.TextField()
#     dob = models.DateField()
#     household_id = models.ForeignKey('Household', on_delete=models.CASCADE, db_column='household_id')
#     educational_qualification = models.TextField()
#     phone_number = models.DecimalField(max_digits=15, decimal_places=0)
#     password = models.CharField(max_length=128)  # Password field
#     # citizen.set_password(raw_password)
    
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password) 
    
#     def check_password(self, raw_password):
#         print(f"Stored password hash: {self.password}")  # Debugging statement
#         print(f"Raw password entered: {raw_password}")
#         # print(self.password)
#         # print(raw_password)
#         # return check_password(raw_password, self.password)
#         return (raw_password==self.password)

    
#     def save(self, *args, **kwargs):
#         """Override save method to hash the password before saving."""
#         if self.password:  # Only hash if a password is provided
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)  # Call the original save method
        
#     def __str__(self):
#         return self.name

# class Household(models.Model):
#     household_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     address = models.TextField()
#     income = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return str(self.household_id)  # Return as string to avoid issues

# class LandRecord(models.Model):
#     land_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     area_acres = models.DecimalField(max_digits=10, decimal_places=2)
#     crop_type = models.TextField()

#     def __str__(self):
#         return str(self.land_id)  # Return as string to avoid issues

# class PanchayatEmployee(models.Model):
#     employee_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     role = models.TextField()
#     password = models.CharField(max_length=128)  # Password field
    
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password) 
    
#     def check_password(self, raw_password):
#         print(f"Stored password hash: {self.password}")  # Debugging statement
#         print(f"Raw password entered: {raw_password}")
#         # print(self.password)
#         # print(raw_password)
#         # return check_password(raw_password, self.password)
#         return (raw_password==self.password)

    
#     def save(self, *args, **kwargs):
#         """Override save method to hash the password before saving."""
#         if self.password:  # Only hash if a password is provided
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)  # Call the original save method
        

#     def __str__(self):
#         return str(self.employee_id)  # Return as string to avoid issues

# class Asset(models.Model):
#     asset_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     type = models.TextField()
#     location = models.TextField()
#     installation_date = models.DateField()
#     panchayat_under = models.TextField()

#     def __str__(self):
#         return str(self.asset_id)  # Return as string to avoid issues

# class WelfareScheme(models.Model):
#     scheme_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     name = models.TextField()
#     description = models.TextField()

#     def __str__(self):
#         return str(self.scheme_id)  # Return as string to avoid issues

# class SchemeEnrollment(models.Model):
#     enrollment_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     scheme_id = models.ForeignKey(WelfareScheme, on_delete=models.CASCADE, db_column='scheme_id')
#     enrollment_date = models.DateField()

#     def __str__(self):
#         return str(self.enrollment_id)  # Return as string to avoid issues

# class CensusData(models.Model):
#     census_data_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     household_id = models.ForeignKey(Household, on_delete=models.CASCADE, db_column='household_id')
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     event_type = models.TextField()
#     event_date = models.DateField()

#     def __str__(self):
#         return f"{self.citizen_id} - {self.event_type}"

# class Tax(models.Model):
#     tax_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     due_date = models.DateField()
#     status = models.TextField()
#     last_paid = models.DateField()

#     def __str__(self):
#         return str(self.tax_id)  # Return as string to avoid issues

# class Complaint(models.Model):
#     complaint_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     complaint = models.TextField()
#     status = models.TextField()
#     remarks = models.TextField()

#     def __str__(self):
#         return str(self.complaint_id)  # Return as string to avoid issues

# class Budget(models.Model):
#     expenditure_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     type = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     status = models.TextField()

#     def __str__(self):
#         return str(self.expenditure_id)  # Return as string to avoid issues

# class GovernmentMonitor(models.Model):
#     monitor_id = models.AutoField(primary_key=True)  # Auto-incremented primary key
#     citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='citizen_id')
#     role = models.TextField()
#     password = models.CharField(max_length=128)  # Password field
    
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password) 
    
#     def check_password(self, raw_password):
#         print(f"Stored password hash: {self.password}")  # Debugging statement
#         print(f"Raw password entered: {raw_password}")
#         # print(self.password)
#         # print(raw_password)
#         # return check_password(raw_password, self.password)
#         return (raw_password==self.password)

    
#     def save(self, *args, **kwargs):
#         """Override save method to hash the password before saving."""
#         if self.password:  # Only hash if a password is provided
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)  # Call the original save method
        

#     def __str__(self):
#         return str(self.monitor_id)  # Return as string to avoid issues