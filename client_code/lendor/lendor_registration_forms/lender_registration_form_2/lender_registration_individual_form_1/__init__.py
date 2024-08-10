from ._anvil_designer import lender_registration_individual_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class lender_registration_individual_form_1(lender_registration_individual_form_1Template):
    company_name_is_valid = False
    organization_type_is_valid = False
    employment_type_is_valid = False
    Occupation_type_is_valid = False
    company_address_is_valid = False
    company_landmark_is_valid = False
    company_ph_no_is_valid = False
    annual_salary_is_valid = False
    designation_is_valid = False
    salary_type_is_valid = False
  
    def __init__(self, user_id, **properties):
        self.userId = user_id
        user_id = int(user_id)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
            self.company_name_text_box.text = user_data['company_name']
            self.organization_type_drop_down.selected_value = user_data['organization_type']
            self.employment_drop_down.selected_value = user_data['employment_type']
            self.occupation_drop_down.selected_value = user_data['occupation_type']
            self.company_add_text_box.text = user_data['company_address']
            self.landmark_text_box.text = user_data['company_landmark']
            self.company_ph_no_text_box.text = user_data['business_no']
            self.annual_salary_text_box.text = user_data['annual_salary']
            self.designation_textbox.text = user_data['designation']
            self.salary_type_drop_down.selected_value = user_data['salary_type']
            # Note: Removed unnecessary user_data.update() here

            options = app_tables.fin_lendor_employee_type.search()
            options_string = [str(option['lendor_employee_type']) for option in options]
            self.employment_drop_down.items = options_string
    
            options = app_tables.fin_lendor_organization_type.search()
            options_string = [str(option['lendor_organization_type']) for option in options]
            self.organization_type_drop_down.items = options_string
    
            options = app_tables.fin_occupation_type.search()
            option_strings = [str(option['occupation_type']) for option in options]
            self.occupation_drop_down.items = option_strings
    
            options_5 = app_tables.fin_lendor_salary_type.search()
            option_strings = [str(option['lendor_salary_type']) for option in options_5]
            self.salary_type_drop_down.items = option_strings

            self.company_name_text_box.add_event_handler('change', self.validate_company_name)
            self.company_add_text_box.add_event_handler('change', self.validate_company_add)
            self.company_ph_no_text_box.add_event_handler('change', self.validate_company_ph_no)
            self.landmark_text_box.add_event_handler('change', self.validate_company_landmark)
            self.designation_textbox.add_event_handler('change', self.validate_employee_designation)
            self.annual_salary_text_box.add_event_handler('change', self.validate_annual_salary)
            self.employee_ID_file_loader.add_event_handler('change', self.validate_file_upload) 
            self.image_1.background = '#FFFFFF'
            self.six_month_bank_statement_file_loader.add_event_handler('change', self.validate_file_upload)
            self.image_2.background = '#FFFFFF'

    def validate_company_name(self, **event_args):
        company_name = self.company_name_text_box.text
        global company_name_is_valid
        if re.match(r'^[A-Za-z][A-Za-z\s]*$', company_name):
            self.company_name_text_box.role = 'outlined'
            company_name_is_valid = True
        else:
            self.company_name_text_box.role = 'outlined-error'
            company_name_is_valid = False
            alert('please enter a valid company name')
          
    def validate_company_ph_no(self, **event_args):
        mobile_no = self.company_ph_no_text_box.text
        global company_ph_no_is_valid
        if re.match(r'^\d{10}$', mobile_no):
            self.company_ph_no_text_box.role = 'outlined'
            company_ph_no_is_valid = True
        elif  ' ' in mobile_no:
            alert('spaces are not allowed')
        else:
            self.company_ph_no_text_box.role = 'outlined-error'  # Red role for invalid input
            company_ph_no_is_valid = False
            alert('please fill total 10 digit correct phnone number')

    def validate_company_add(self, **event_args):
          comp_add = self.company_add_text_box.text
          global company_address_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', comp_add):
              self.company_add_text_box.role = 'outlined'
              company_address_is_valid = True
          else:
              self.company_add_text_box.role = 'outlined-error'
              alert('please enter a valid business address')
              company_address_is_valid = False
              

    def validate_company_landmark(self, **event_args):
          company_landmark = self.landmark_text_box.text
          global company_landmark_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', company_landmark):
              self.landmark_text_box.role = 'outlined'
              company_landmark_is_valid = True
          else:
              self.landmark_text_box.role = 'outlined-error'
              alert('please enter a valid business address')
              company_landmark_is_valid = False

    def validate_employee_designation(self, **event_args):
          employee_designation = self.designation_textbox.text
          global designation_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', employee_designation):
              self.designation_textbox.role = 'outlined'
              designation_is_valid = True
          else:
              self.designation_textbox.role = 'outlined-error'
              alert('please enter a valid business address')
              designation_is_valid = False

    def validate_annual_salary(self, **event_args):
          Annual_salary = self.annual_salary_text_box.text
          global annual_salary_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', Annual_salary):
              self.annual_salary_text_box.role = 'outlined'
              annual_salary_is_valid = True
          elif ' ' in Annual_salary:
              alert('Spaces are not allowed')
          else:
              self.annual_salary_text_box.role = 'outlined-error'
              alert('please enter a valid business address')    
              annual_salary_is_valid = False
    
    def validate_file_upload(self, **event_args):
        file_loader = event_args['sender']
        file = file_loader.file
        max_size = 2 * 1024 * 1024  # 2MB in bytes
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
    
        if file:
            file_size = len(file.get_bytes())
            if file_size > max_size:
                alert('File size should be less than 2MB')
                file_loader.clear()
                return
    
            if file.content_type not in allowed_types:
                alert('Invalid file type. Only JPEG, PNG, jpg and PDF are allowed')
                file_loader.clear()
                return

    def next_click(self, **event_args):     
        self.validate_company_name()
        self.validate_company_add()
        self.validate_annual_salary()
        self.validate_company_landmark()
        self.validate_employee_designation()
        self.validate_company_ph_no()
        company_name = self.company_name_text_box.text    
        org_type = self.organization_type_drop_down.selected_value
        emp_type = self.employment_drop_down.selected_value
        occupation_type = self.occupation_drop_down.selected_value
        comp_address = self.company_add_text_box.text
        landmark = self.landmark_text_box.text
        business_phone_number = self.company_ph_no_text_box.text
        annual_salary = self.annual_salary_text_box.text
        designation = self.designation_textbox.text
        emp_id_proof = self.employee_ID_file_loader.file
        last_six_month = self.six_month_bank_statement_file_loader.file
        salary_type = self.salary_type_drop_down.selected_value
        global organization_type_is_valid
        global employment_type_is_valid
        global Occupation_type_is_valid
        global salary_type_is_valid

        if not org_type:
          organization_type_is_valid = False
          self.organization_type_drop_down.role = 'outlined-error'
          self.organization_type_drop_down.focus()
        else:
          organization_type_is_valid = True
          self.organization_type_drop_down.role = 'outlined'
          
        if not emp_type:
          employment_type_is_valid = False
          self.employment_drop_down.role = 'outlined-error'
          self.employment_drop_down.focus()
          Notification('please fill all details')
        else:
          employment_type_is_valid = True
          self.employment_drop_down.role = 'outlined'
          

        if not occupation_type:
          Occupation_type_is_valid = False
          self.occupation_drop_down.role = 'outlined-error'
          self.occupation_drop_down.focus()
          Notification('please fill all details')
        else:
          self.occupation_drop_down.role = 'outlined'
          Occupation_type_is_valid = True

        if not salary_type:
          salary_type_is_valid = False
          self.salary_type_drop_down.role = 'outlined-error'
          self.salary_type_drop_down.focus()
          Notification('please fill all details')
        else:
          self.salary_type_drop_down.role = 'outlined'
          salary_type_is_valid = True

        if not emp_id_proof:
          self.employee_ID_file_loader.background = 'red'
          self.employee_ID_file_loader.focus()
          Notification('please fill all the details')
          return
        else:
          self.employee_ID_file_loader.role = 'outlined'
          self.image_1.background = '#FFFFFF'

        if not last_six_month:
          self.six_month_bank_statement_file_loader.background = 'red'
          self.six_month_bank_statement_file_loader.focus()
          Notification('please fill all the details')
          return
        else:
          self.six_month_bank_statement_file_loader.role = 'outlined'
          self.image_2.background = '#FFFFFF'
          
        user_id = self.userId 
      
        global company_name_is_valid
        global company_address_is_valid
        global company_landmark_is_valid
        global company_ph_no_is_valid
        global annual_salary_is_valid
        global designation_is_valid
    
        if company_name_is_valid and company_name_is_valid and company_landmark_is_valid and company_ph_no_is_valid and annual_salary_is_valid and designation_is_valid and organization_type_is_valid and employment_type_is_valid and Occupation_type_is_valid and salary_type_is_valid:
          anvil.server.call('add_lendor_individual_form_1', company_name, org_type, emp_type, occupation_type, self.userId)
          anvil.server.call('add_lendor_individual_form_2', comp_address, landmark, business_phone_number, self.userId)
          anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, self.userId, salary_type)
          open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details', user_id=self.userId)
         
        else:
          alert('please fill all the details')
            
    
    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("bank_users.user_form")

    def employee_ID_file_loader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.employee_id_label.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_1.source = self.employee_ID_file_loader.file
                self.image_1.background = '#FFFFFF'
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_1.source = '_/theme/bank_users/default%20pdf.png'
                self.image_1.background = '#FFFFFF'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                
                self.image_1.clear()

    def six_month_bank_statement_file_loader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.six_month_bank_label.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_2.source = self.six_month_bank_statement_file_loader.file
                self.image_2.background = '#FFFFFF'
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_2.source = '_/theme/bank_users/default%20pdf.png'
                self.image_2.background = '#FFFFFF'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                
                self.image_2.clear()

    def prev_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor.lendor_registration_forms.lender_registration_form_2', user_id=self.userId)





 
    

