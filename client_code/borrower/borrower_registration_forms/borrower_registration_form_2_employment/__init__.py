from ._anvil_designer import borrower_registration_form_2_employmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re
from datetime import date, datetime

class borrower_registration_form_2_employment(borrower_registration_form_2_employmentTemplate):
    yearly_income_is_valid = False
    crop_name_is_valid = False
    acres_of_land_is_valid = False
    type_of_land_valid = False
  
    student_college_name = False
    student_id = False
    student_address = False
    student_proof = False
    no_of_employes_type_is_valid = False
    registered_off_add_is_valid = False
    crop_name_is_valid = False
    annual_income_is_valid = False
    # annual_salary_is_valid = False
    # designation_is_valid = False
    # company_landmark_is_valid = False
    # company_address_is_valid = False
    # company_ph_no_is_valid = False
    company_name_is_valid = False
    # occupation_type_is_valid = False
    business_name_is_valid = False
    business_add_is_valid = False
    business_type_is_valid = False
    year_estd_is_valid = False
    industry_type_is_valid = False
    six_month_turn_over_is_valid = False
    cin_is_valid = False
    din_is_valid = False
    registered_off_add_is_valid = False
    # lendor_business_type_is_valid = False  
    employees_working_is_valid = False

    company_name_is_valid = False
    organization_type_is_valid = False
    employment_type_is_valid = False
    occupation_type_is_valid = False
    company_address_is_valid = False
    company_landmark_is_valid = False
    company_ph_no_is_valid = False
    annual_salary_is_valid = False
    designation_is_valid = False
    salary_type_is_valid = False
  
    def __init__(self, user_id, **properties):
        
        # super().__init__(**properties)        
        self.user_id = user_id
        
        # Initialize all grid panels as invisible
        self.column_panel_1.visible = False
        self.column_panel_22.visible = False
        self.column_panel_3.visible = False
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Fetch user data from the database
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        
        if user_data:
            # Populate form fields if user data exists
            
            self.text_box_1_copy.text=user_data['company_name']
            self.drop_down_3.selected_value=user_data['organization_type']
            self.drop_down_1_copy.selected_value=user_data['employment_type']
            self.drop_down_2_copy.selected_value = user_data['occupation_type']
            self.text_box_1_copy_2.text=user_data['company_address']
            self.text_box_3_copy.text=user_data['company_landmark']
            self.text_box_2_copy.text=user_data['business_no']
            self.text_box_1_copy_3.text=user_data['annual_salary']
            self.text_box_2_copy_2.text=user_data['designation']
            self.drop_down_1_copy_2.selected_value = user_data['salary_type']
          
            self.text_box_1.text = user_data['business_add']
            self.text_box_2.text = user_data['business_name']
            self.drop_down_12.selected_value = user_data['business_type']
            self.date_picker_1.date = user_data['year_estd']
            self.text_box_3.text = user_data['industry_type']
            self.text_box_4.text = user_data['six_month_turnover']      
          
            self.text_box_5.text = user_data['din'].replace(' ', '') if 'din' in user_data else ''
            self.text_box_6.text = user_data['cin'].replace(' ', '') if 'cin' in user_data else ''
            self.text_box_7.text = user_data['registered_off_add'] if 'registered_off_add' in user_data else ''
          
            self.borrower_college_name_text.text = user_data['college_name']
            self.borrower_college_id_text.text=user_data['college_id']
            self.borrower_college_address_text.text=user_data['college_address']
          
            self.drop_down_1_copy_3.selected_value = user_data['land_type']
            self.text_box_1_copy_4.text = str(user_data['total_acres'])  # Convert to string
            self.text_box_2_copy_3.text = user_data['crop_name']
            self.text_box_3_copy_2.text = user_data['farmer_earnings']

            options_2 = app_tables.fin_borrower_land_type.search()
            option_strings_2 = [str(option['land_type']) for option in options_2]
            self.drop_down_1_copy_3.items = option_strings_2

            options_1 = app_tables.fin_borrower_employee_type.search()
            option_strings_1 = [str(option['borrower_employee_type']) for option in options_1]
            self.drop_down_1_copy.items = option_strings_1
        
            # Populate drop_down_3 with data from 'organization_type' column
            options_3 = app_tables.fin_borrower_organization_type.search()
            option_strings_2 = [str(option['borrower_organization_type']) for option in options_3]
            self.drop_down_3.items = option_strings_2
        
            options_4 = app_tables.fin_occupation_type.search()
            option_strings = [str(option['occupation_type']) for option in options_4]
            self.drop_down_2_copy.items = option_strings

            options_5 = app_tables.fin_borrower_salary_type.search()
            option_strings = [str(option['borrower_salary_type']) for option in options_5]
            self.drop_down_1_copy_2.items = option_strings

            options_6 = app_tables.fin_borrower_business_type.search()
            option_strings_1 = [str(option['borrower_business_type']) for option in options_6]
            self.drop_down_12.items = option_strings_1
            
            # Handle initial visibility based on user type
            user_type = user_data['user_type'] if 'user_type' in user_data else ''
            self.update_visibility(user_type)
            self.text_box_1_copy.add_event_handler('change', self.validate_company_name)
            self.text_box_1_copy_2.add_event_handler('change', self.validate_company_add)
            self.text_box_2_copy.add_event_handler('change', self.validate_company_ph_no)
            self.text_box_3_copy.add_event_handler('change', self.validate_company_landmark)
            self.text_box_2_copy_2.add_event_handler('change', self.validate_employee_designation)
            self.text_box_1_copy_3.add_event_handler('change', self.validate_annual_salary)
            self.file_loader_1_copy_2.add_event_handler('change', self.employee_ID_file_loader_change)
            self.file_loader_2.add_event_handler('change', self.six_month_bank_statement_file_loader_change)
            self.drop_down_2_copy.add_event_handler('change', self.validate_occupation_type)
            self.drop_down_3.add_event_handler('change', self.validate_organization_type)
          
            self.text_box_1.add_event_handler('change', self.validate_business_add)
            self.text_box_2.add_event_handler('change', self.validate_business_name)
            self.date_picker_1.add_event_handler('change', self.validate_year_estd)
            self.text_box_3.add_event_handler('change', self.validate_industry_type)
            self.text_box_4.add_event_handler('change', self.validate_six_month_turnover)
            self.text_box_5.add_event_handler('change', self.validate_din)
            self.text_box_6.add_event_handler('change', self.validate_cin)
            self.text_box_7.add_event_handler('change', self.validate_registered_off_add)
            self.drop_down_4.add_event_handler('change', self.validate_no_of_employes)
            self.drop_down_12.add_event_handler('change', self.validate_business_type)
            self.file_loader_1.add_event_handler('change', self.file_loader)
            self.file_loader_1_copy.add_event_handler('change', self.file_loader_1_copy1)

            self.text_box_1_copy_4.add_event_handler('change', self.acres_of_land)
            self.text_box_3_copy_2.add_event_handler('change',self.yearly_income)
            self.text_box_2_copy_3.add_event_handler('change',self.validate_crop_name)
            self.drop_down_1_copy_3.add_event_handler('change', self.validate_type_of_land)

            self.borrower_college_address_text.add_event_handler('change',self.validate_borrower_college_address)
            self.borrower_college_id_text.add_event_handler('change', self.validate_borrower_college_id)
            self.borrower_college_name_text.add_event_handler('change', self.validate_borrower_college_name)
            self.borrower_college_proof_img.add_event_handler('change', self.borrower_college_proof_img_change)

            
        else:
            print(f"No user data found for user_id: {user_id}")
            # Handle case where user_data is None or not found
        
        # Set up event handler for dropdown change
        self.drop_down_1.set_event_handler('change', self.drop_down_1_change_handler)
        
        # Initialize visibility of components inside grid_panel_3
        self.drop_down_2.visible = True
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Set up event handler for drop_down_2 change
        self.drop_down_2.set_event_handler('change', self.drop_down_2_change_handler)

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
    
    def update_visibility(self, user_type):
        # Reset all grid panel visibilities
        self.column_panel_1.visible = False
        self.column_panel_22.visible = False
        self.column_panel_3.visible = False
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Set visibility based on user_type
        if user_type == 'Student':
            
            self.column_panel_1.visible = True
        elif user_type == 'Employee':
            self.column_panel_22.visible = True
        elif user_type == 'Self Employement':
            self.column_panel_3.visible = True
        else:
            # Handle other user types or default case
            pass
    
    def drop_down_1_change_handler(self, **event_args):
        selected_value = self.drop_down_1.selected_value
        self.update_visibility(selected_value)
    
    def drop_down_2_change_handler(self, **event_args):
        selected_value = self.drop_down_2.selected_value
        
        if selected_value == 'Business':  # Replace with your actual dropdown values
            self.column_panel_4.visible = True
            self.column_panel_5.visible = False
        elif selected_value == 'Farmer':  # Replace with your actual dropdown values
            self.column_panel_4.visible = False
            self.column_panel_5.visible = True
        else:
            self.column_panel_4.visible = False
            self.column_panel_5.visible = False

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.borrower_registration_forms.borrower_registration_form_1_education',self.user_id)

    def button_1_next_click(self, **event_args):

        """This method is called when the button is clicked"""
    
        # Centralized validation check function
        def validate_all(validations):
            for validation in validations:
                if not validation():
                    return False
            return True
        
        # Validations for different selections
        if self.drop_down_1.selected_value == 'Student':
          global student_college_name 
          global student_id
          global student_address
          global student_proof
          
          student_college_name = self.borrower_college_name_text.text
          student_id = self.borrower_college_id_text.text
          student_address = self.borrower_college_address_text.text
          student_proof = self.borrower_college_proof_img.file
          user_id = self.user_id
          
          if not student_proof:
            self.borrower_college_proof_img.background = 'red'
            self.borrower_college_proof_img.focus()
            alert('please fill all the details.')
            # student_proof = False
          else:
            self.borrower_college_proof_img.background = 'outlined'
            # student_proof = True
            if student_college_name and student_id and student_address:
              anvil.server.call('add_borrower_student',student_college_name,student_id,student_proof,student_address,user_id)
              open_form('borrower.borrower_registration_forms.borrower_registration_form_3_marital', self.user_id)
            else:
              alert('Please fill all the details')
        
        elif self.drop_down_1.selected_value == 'Employee':
          user_id = self.user_id
          self.validate_company_name()
          self.validate_company_add()
          self.validate_annual_salary()
          self.validate_company_landmark()
          self.validate_employee_designation()
          self.validate_company_ph_no()
          company_name = self.text_box_1_copy.text    
          org_type = self.drop_down_3.selected_value
          emp_type = self.drop_down_1_copy.selected_value
          occupation_type = self.drop_down_2_copy.selected_value
          comp_address = self.text_box_1_copy_2.text
          landmark = self.text_box_3_copy.text
          business_phone_number = self.text_box_2_copy.text
          annual_salary = self.text_box_1_copy_3.text
          designation = self.text_box_2_copy_2.text
          emp_id_proof = self.file_loader_1_copy_2.file
          last_six_month = self.file_loader_2.file
          salary_type = self.drop_down_1_copy_2.selected_value
          global organization_type_is_valid
          global employment_type_is_valid
          global occupation_type_is_valid
          global salary_type_is_valid
  
          if not org_type:
            organization_type_is_valid = False
            self.drop_down_3.role = 'outlined-error'
            self.drop_down_3.focus()
          else:
            organization_type_is_valid = True
            self.drop_down_3.role = 'outlined'
            
          if not emp_type:
            employment_type_is_valid = False
            self.drop_down_1_copy.role = 'outlined-error'
            self.drop_down_1_copy.focus()
            Notification('please fill all details')
          else:
            employment_type_is_valid = True
            self.drop_down_1_copy.role = 'outlined'
            
  
          if not occupation_type:
            Occupation_type_is_valid = False
            self.drop_down_2_copy.role = 'outlined-error'
            self.drop_down_2_copy.focus()
            Notification('please fill all details')
          else:
            self.drop_down_2_copy.role = 'outlined'
            Occupation_type_is_valid = True
  
          if not salary_type:
            salary_type_is_valid = False
            self.drop_down_1_copy_2.role = 'outlined-error'
            self.drop_down_1_copy_2.focus()
            Notification('please fill all details')
          else:
            self.drop_down_1_copy_2.role = 'outlined'
            salary_type_is_valid = True
  
          if not emp_id_proof:
            self.file_loader_1_copy_2.background = 'red'
            self.file_loader_1_copy_2.focus()
            Notification('please fill all the details')
            return
          else:
            self.file_loader_1_copy_2.role = 'outlined'
  
          if not last_six_month:
            self.file_loader_2.background = 'red'
            self.file_loader_2.focus()
            Notification('please fill all the details')
            return
          else:
            self.file_loader_2.role = 'outlined'
            
        
          global company_name_is_valid
          global company_address_is_valid
          global company_landmark_is_valid
          global company_ph_no_is_valid
          global annual_salary_is_valid
          global designation_is_valid
      
          if company_name_is_valid and company_name_is_valid and company_landmark_is_valid and company_ph_no_is_valid and annual_salary_is_valid and designation_is_valid and organization_type_is_valid and employment_type_is_valid and Occupation_type_is_valid and salary_type_is_valid:
            anvil.server.call('add_lendor_individual_form_1', company_name,org_type,emp_type,occupation_type,user_id)
            anvil.server.call('add_lendor_individual_form_2',comp_address,landmark,business_phone_number,user_id)
            anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, user_id,salary_type )
            open_form('borrower.borrower_registration_forms.borrower_registration_form_3_marital', self.user_id)
          
          else:
            alert('please fill all the details')
              
                  
        
        elif self.drop_down_1.selected_value == 'Self Employement':
            if self.drop_down_2.selected_value == 'Farmer':
              global yearly_income_is_valid
              global crop_name_is_valid
              global acres_of_land_is_valid
              global type_of_land_valid

              type_of_land_valid = self.drop_down_1_copy_3.selected_value
              acres_of_land_is_valid = self.text_box_1_copy_4.text
              crop_name_is_valid = self.text_box_2_copy_3.text
              yearly_income_is_valid = self.text_box_3_copy_2.text
              user_id = self.user_id
              if yearly_income_is_valid and crop_name_is_valid and acres_of_land_is_valid and type_of_land_valid:
                anvil.server.call('add_borrower_farmer', type_of_land_valid, acres_of_land_is_valid, crop_name_is_valid, yearly_income_is_valid, user_id)            
                open_form('borrower.borrower_registration_forms.borrower_registration_form_3_marital', self.user_id)
              else:
                alert('Please fill all the details')
            elif self.drop_down_2.selected_value == 'Business':

              user_id = self.user_id 
              global business_name_is_valid
              global business_add_is_valid
              global industry_type_is_valid
              global six_month_turn_over_is_valid
              global din_is_valid
              global cin_is_valid
              global registered_off_add_is_valid

              business_name_is_valid = self.text_box_2.text
              business_add_is_valid = self.text_box_1.text
              business_type = self.drop_down_12.selected_value
              empolyees_working = self.drop_down_4.selected_value
              din_is_valid = self.text_box_5.text
              cin_is_valid = self.text_box_6.text
              registered_off_add_is_valid = self.text_box_7.text
              proof_verification = self.file_loader_1_copy.file
              year = self.date_picker_1.date
              six_month_turn_over_is_valid = self.file_loader_1.file
              industry_type_is_valid = self.text_box_3.text
              turn_over = self.text_box_4.text
              months = None
              if not empolyees_working :
                employees_working_is_valid = False
                self.drop_down_4.role = 'outlined-error'
                self.drop_down_4.focus()
                Notification('please fill all details')
              else:
                employees_working_is_valid = True
              if not business_type:
                business_type_is_valid = False
                self.drop_down_12.role = 'outlined-error'
                self.drop_down_12.focus()
                Notification('please fill all details')
              else:
                business_type_is_valid = True


              if not six_month_turn_over_is_valid:
                    self.file_loader_1.background = 'red'
                    self.file_loader_1.focus()
                    Notification('Please fill all details').show()
                    return
              else:
                    self.file_loader_1.role = 'outlined'
              
              if not proof_verification:
                    self.file_loader_1_copy.background = 'red'
                    self.file_loader_1_copy.focus()
                    Notification('Please fill all details').show()
                    return
              else:
                  self.file_loader_1_copy.role = 'outlined'

              if business_name_is_valid and six_month_turn_over_is_valid and empolyees_working and proof_verification and business_add_is_valid and industry_type_is_valid and six_month_turn_over_is_valid and din_is_valid and cin_is_valid and registered_off_add_is_valid and business_type_is_valid and employees_working_is_valid:
                anvil.server.call('add_lendor_institutional_form_1',business_name_is_valid,business_add_is_valid,business_type,empolyees_working,user_id)
                anvil.server.call('add_lendor_institutional_form_3', din_is_valid, cin_is_valid, registered_off_add_is_valid, proof_verification, user_id)
                anvil.server.call('add_lendor_institutional_form_2', year, months, industry_type_is_valid, turn_over, six_month_turn_over_is_valid, user_id)
                open_form('borrower.borrower_registration_forms.borrower_registration_form_3_marital', self.user_id)
              else :
                  alert('please fill all the details')
                    
        else:
            pass

  
    # def borrower_college_proof_img_change(self, file, **event_args):
    #     """This method is called when a new file is loaded into this FileLoader"""
    #     valid, message = self.validate_file(file)
    #     if valid:
    #       self.image_1_copy_2.source = file
    #     else:
    #       Notification(message).show()
    #       self.borrower_college_proof_img.clear()

    # def file_loader_1_change(self, file, **event_args):
    #     """This method is called when a new file is loaded into this FileLoader"""
    #     valid, message = self.validate_file(file)
    #     if valid:
    #       self.image_1_copy_3.source = file
    #     else:
    #       Notification(message).show()
    #       self.file_loader_1_copy_2.clear()

    # def file_loader_2_change(self, file, **event_args):
    #     """This method is called when a new file is loaded into this FileLoader"""
    #     valid, message = self.validate_file(file)
    #     if valid:
    #       self.image_2.source = file
    #     else:
    #       Notification(message).show()
    #       self.file_loader_2.clear()

    # def file_loader_1(self, file, **event_args):
    #     """This method is called when a new file is loaded into this FileLoader"""
    #     if file:
    #         self.user_photo_file_name.text = file.name if file else ''
    #         content_type = file.content_type
            
    #         if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
    #             # Display the image directly
    #             self.image_profile.source = self.registration_img_file_loader.file
    #         elif content_type == 'application/pdf':
    #             # Display a default PDF image temporarily
    #             self.image_profile.source = '_/theme/bank_users/default%20pdf.png'
    #         else:
    #             alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
    #             self.registration_img_file_loader.clear()

    def validate_cin(self, **event_args):
        cin = self.text_box_6.text.strip()
        global cin_is_valid
    
        # Validate CIN to contain only alphanumeric characters
        if re.match(r'^[a-zA-Z0-9]+$', cin):
            self.text_box_6.role = 'outlined'
            cin_is_valid = True
        elif ' ' in cin:
            alert('Spaces are not allowed in CIN')
        else:
            self.text_box_6.role = 'outlined-error'
            cin_is_valid = False
            alert('Please enter a valid CIN number containing only letters and numbers')
  
    def validate_din(self, **event_args):
        din = self.text_box_5.text.strip()
        global din_is_valid
    
        # Validate DIN to contain only alphanumeric characters
        if re.match(r'^[a-zA-Z0-9]+$', din):
            self.text_box_5.role = 'outlined'
            din_is_valid = True
        elif ' ' in din:
            alert('Spaces are not valid in DIN')
        else:
            self.text_box_5.role = 'outlined-error'
            din_is_valid = False
            alert("Please enter a valid DIN number containing only letters and numbers")
  
    def validate_six_month_turnover(self, **event_args):
          six_month_turnover = self.text_box_4.text
          global six_month_turn_over_is_valid
          if re.match(r'^\d+$', six_month_turnover):
              self.text_box_4.role = 'outlined'
              six_month_turn_over_is_valid = True
          elif ' 'in six_month_turnover:
              alert('Spaces are not allowed ')
          else:
              self.text_box_4.role = 'outlined-error'
              six_month_turn_over_is_valid = False
              alert('please enter a valid six month turn over')

    def validate_registered_off_add(self, **event_args):
          registered_off_add = self.text_box_7.text
          global registered_off_add_is_valid
          if re.match(r'^[A-Za-z\s]+$', registered_off_add):
              self.text_box_7.role = 'outlined'
              registered_off_add_is_valid = True
          else:
              self.text_box_7.role = 'outlined-error'
              registered_off_add_is_valid = False
              alert('please enter a valid registered office address')

    
    def validate_industry_type(self, **event_args):
          industry_type = self.text_box_3.text
          global industry_type_is_valid 
          if re.match(r'^[A-Za-z][A-Za-z\s]*$', industry_type):
              self.text_box_3.role = 'outlined'
              industry_type_is_valid = True
          else:
              self.text_box_3.role = 'outlined-error'
              industry_type_is_valid = False
              alert('please enter a valid industry type')

    def validate_business_name(self, **event_args):
          global business_name_is_valid
          business_name = self.text_box_2.text        
          if re.match(r'^[A-Za-z][A-Za-z\s]*$', business_name):
              self.text_box_2.role = 'outlined'            
              business_name_is_valid = True
          else:
              self.text_box_2.role = 'outlined-error'
              business_name_is_valid = False
              alert('please enter a valid business name')
          # Get today's date


              
    def validate_year_estd(self, **event_args):
      year = self.date_picker_1.date  # Ensure self.date_picker_1.date is returning a datetime object
      today = datetime.today()
      global year_estd_is_valid
      
      if not year:
          self.date_picker_1.role = 'outlined-error'
          year_estd_is_valid = False
          alert('Please enter a valid year of establishment')
          return
      
      if year.year > today.year:
          alert("The year cannot be in the future. Please select a valid year.", title="Invalid Year")
          self.date_picker_1.role = 'outlined-error'
          year_estd_is_valid = False
          return
      elif year.year == today.year and year.month > today.month:
          alert("The month cannot be in the future. Please select a valid month.", title="Invalid Month")
          self.date_picker_1.role = 'outlined-error'
          year_estd_is_valid = False
          return
      elif year.year == today.year and year.month == today.month and year.day > today.day:
          alert("The date cannot be in the future. Please select a valid date.", title="Invalid Date")
          self.date_picker_1.role = 'outlined-error'
          year_estd_is_valid = False
          return
  
      self.date_picker_1.role = 'outlined'
      year_estd_is_valid = True


    def validate_business_type(self, **event_args):
          Business_type = self.drop_down_12.selected_value
          global business_type_is_valid
          if Business_type is not None:
              self.drop_down_12.role = 'outlined'
              business_type_is_valid = True
          else:
              self.drop_down_12.role = 'outlined-error'
              business_type_is_valid = False
              alert('please enter a valid business type')


    def validate_no_of_employes(self, **event_args):
          No_of_employes = self.drop_down_4.selected_value
          global no_of_employes_type_is_valid
          if No_of_employes is not None:
              self.drop_down_4.role = 'outlined'
              no_of_employes_type_is_valid = True
          else:
              self.drop_down_4.role = 'outlined-error'
              no_of_employes_type_is_valid = False
              alert('please enter a valid employes count')

    def validate_occupation_type(self, **event_args):
          No_of_employes = self.drop_down_2_copy.selected_value
          global occupation_type_is_valid
          if No_of_employes is not None:
              self.drop_down_2_copy.role = 'outlined'
              occupation_type_is_valid = True
          else:
              self.drop_down_2_copy.role = 'outlined-error'
              occupation_type_is_valid = False
              alert('please enter a valid occupation type')

    def validate_organization_type(self, **event_args):
          No_of_employes = self.drop_down_3.selected_value
          global organization_type_is_valid
          if No_of_employes is not None:
              self.drop_down_3.role = 'outlined'
              organization_type_is_valid = True
          else:
              self.drop_down_3.role = 'outlined-error'
              organization_type_is_valid = False
              alert('please enter a valid organization type')

  

    def file_loader(self, file, **event_args):
          """This method is called when a new file is loaded into this FileLoader"""
          if file:
                  self.label_6.text = file.name if file else ''
                  content_type = file.content_type
                  
                  if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                      # Display the image directly
                      self.image_1.source = self.file_loader_1.file
                  elif content_type == 'application/pdf':
                      # Display a default PDF image temporarily
                      self.image_1.source = '_/theme/bank_users/default%20pdf.png'
                  else:
                      alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                      self.file_loader_1.clear()
  
    def file_loader_1_copy1(self, file, **event_args):
          """This method is called when a new file is loaded into this FileLoader"""
          if file:
                    self.label_7.text = file.name if file else ''
                    content_type = file.content_type
                    
                    if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                        # Display the image directly
                        self.image_1_copy.source = self.file_loader_1_copy.file
                    elif content_type == 'application/pdf':
                        # Display a default PDF image temporarily
                        self.image_1_copy.source = '_/theme/bank_users/default%20pdf.png'
                    else:
                        alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                        self.file_loader_1_copy.clear()


    def validate_business_add(self, **event_args):
          Business_add = self.text_box_1.text
          global business_add_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', Business_add):
              self.text_box_1.role = 'outlined'
              business_add_is_valid = True
          else:
              self.text_box_1.role = 'outlined-error'
              business_add_is_valid = False
              alert('please enter a valid business address')


    def validate_company_name(self, **event_args):
        company_name = self.text_box_1_copy.text
        global company_name_is_valid
        if re.match(r'^[A-Za-z][A-Za-z\s]*$', company_name):
            self.text_box_1_copy.role = 'outlined'
            company_name_is_valid = True
        else:
            self.text_box_1_copy.role = 'outlined-error'
            company_name_is_valid = False
            alert('please enter a valid company name')


    def acres_of_land(self, **event_args):
          six_month_turnover = self.text_box_1_copy_4.text
          global acres_of_land_is_valid
          if re.match(r'^\d+$', six_month_turnover):
              self.text_box_1_copy_4.role = 'outlined'
              acres_of_land_is_valid = True
          elif ' 'in six_month_turnover:
              alert('Spaces are not allowed ')
          else:
              self.text_box_1_copy_4.role = 'outlined-error'
              acres_of_land_is_valid = False
              alert('please enter a valid acres of land')

########
    def employee_ID_file_loader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.label_8.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_1_copy_3.source = self.file_loader_1_copy_2.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_1_copy_3.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.image_1_copy_3.background = 'red'
                self.image_1_copy_3.clear()

    def six_month_bank_statement_file_loader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.label_9.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_2.source = self.file_loader_2.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_2.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.image_2.background = 'red'
                self.image_2.clear()


          
    def validate_company_ph_no(self, **event_args):
        mobile_no = self.text_box_2_copy.text
        global company_ph_no_is_valid
        if re.match(r'^\d{10}$', mobile_no):
            self.text_box_2_copy.role = 'outlined'
            company_ph_no_is_valid = True
        elif  ' ' in mobile_no:
            alert('spaces are not allowed')
        else:
            self.text_box_2_copy.role = 'outlined-error'  # Red role for invalid input
            company_ph_no_is_valid = False
            alert('please fill total 10 digit correct phnone number')

    def validate_company_add(self, **event_args):
          comp_add = self.text_box_1_copy_2.text
          global company_address_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', comp_add):
              self.text_box_1_copy_2.role = 'outlined'
              company_address_is_valid = True
          else:
              self.text_box_1_copy_2.role = 'outlined-error'
              alert('please enter a valid company address')
              company_address_is_valid = False
              

    def validate_company_landmark(self, **event_args):
          company_landmark = self.text_box_3_copy.text
          global company_landmark_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', company_landmark):
              self.text_box_3_copy.role = 'outlined'
              company_landmark_is_valid = True
          else:
              self.text_box_3_copy.role = 'outlined-error'
              alert('please enter a valid company landmark')
              company_landmark_is_valid = False

    def validate_employee_designation(self, **event_args):
          employee_designation = self.text_box_2_copy_2.text
          global designation_is_valid
          if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', employee_designation):
              self.text_box_2_copy_2.role = 'outlined'
              designation_is_valid = True
          else:
              self.text_box_2_copy_2.role = 'outlined-error'
              alert('please enter a valid designation')
              designation_is_valid = False

    def validate_annual_salary(self, **event_args):
        annual_salary = self.text_box_1_copy_3.text.strip()
        global annual_salary_is_valid
        
        # Regex to validate that the annual salary contains only numeric characters
        if re.match(r'^\d+$', annual_salary):
            self.text_box_1_copy_3.role = 'outlined'
            annual_salary_is_valid = True
        else:
            self.text_box_1_copy_3.role = 'outlined-error'
            alert('Please enter a valid annual salary with only numeric characters.')
            annual_salary_is_valid = False

    # def validate_file_upload(self, **event_args):
    #     file_loader = event_args['sender']
    #     file = file_loader.file
    #     max_size = 2 * 1024 * 1024  # 2MB in bytes
    #     allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
    
    #     if file:
    #         file_size = len(file.get_bytes())
    #         if file_size > max_size:
    #             alert('File size should be less than 2MB')
    #             file_loader.clear()
    #             return
    
    #         if file.content_type not in allowed_types:
    #             alert('Invalid file type. Only JPEG, PNG, jpg and PDF are allowed')
    #             file_loader.clear()
    #             return


    def yearly_income(self, **event_args):
        annual_salary = self.text_box_3_copy_2.text.strip()
        global yearly_income_is_valid
        
        # Regex to validate that the annual salary contains only numeric characters
        if re.match(r'^\d+$', annual_salary):
            self.text_box_3_copy_2.role = 'outlined'
            yearly_income_is_valid = True
        else:
            self.text_box_3_copy_2.role = 'outlined-error'
            alert('Please enter a valid annual income with only numeric characters.')
            yearly_income_is_valid = False
    
    def validate_crop_name(self, **event_args):
        crop_name = self.text_box_2_copy_3.text.strip()
        global crop_name_is_valid
    
        # Validate crop name to contain only alphanumeric characters
        if re.match(r'^[a-zA-Z0-9]+$', crop_name):
            self.text_box_2_copy_3.role = 'outlined'
            crop_name_is_valid = True
        else:
            self.text_box_2_copy_3.role = 'outlined-error'
            crop_name_is_valid = False
            alert("Please enter a valid crop name")


    def validate_borrower_college_address(self, **event_args):
        address = self.borrower_college_address_text.text.strip()
        global student_address
    
        # Regex to validate that the address contains only alphanumeric characters, spaces, and specific punctuation marks
        if re.match(r'^[A-Za-z0-9\s,().?]+$', address):
            self.borrower_college_address_text.role = 'outlined'  # Valid address
            student_address = True
        else:
            self.borrower_college_address_text.role = 'outlined-error'  # Invalid address
            student_address = False
            alert('Invalid address format. Please enter a valid address with only letters, numbers, spaces, and these punctuation marks: , ( ) ? .')



    def validate_borrower_college_id(self, **event_args):
        address = self.borrower_college_id_text.text.strip()
        global student_id
    
        # Regex to validate that the address contains only alphanumeric characters and spaces
        if re.match(r'^[A-Za-z0-9\s]+$', address):
            self.borrower_college_id_text.role = 'outlined'
            student_id = True# Valid address
        else:
            self.borrower_college_id_text.role = 'outlined-error'
            student_id = False# Invalid address
            alert('Invalid ID format. Please enter a valid ID with only letters, numbers, and spaces.')


    def validate_borrower_college_name(self, **event_args):
        college_name = self.borrower_college_name_text.text.strip()
        global student_college_name 
        
        if re.match(r'^[A-Za-z0-9\s]+$', college_name):
            self.borrower_college_name_text.role = 'outlined'  # Valid college name
            student_college_name = True
        else:
            self.borrower_college_name_text.role = 'outlined-error'
            student_college_name = False
            alert('Invalid college name format. Please enter a valid college name with only letters, numbers, and spaces.')

    def borrower_college_proof_img_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.college_label.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.college_img.source = self.borrower_college_proof_img.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.college_img.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.college_img.background = 'red'
                self.college_img.clear()

    def validate_type_of_land(self, **event_args):
          Business_type = self.drop_down_1_copy_3.selected_value
          global type_of_land_valid
          if Business_type is not None:
              self.drop_down_1_copy_3.role = 'outlined'
              type_of_land_valid = True
          else:
              self.drop_down_1_copy_3.role = 'outlined-error'
              type_of_land_valid = False
              alert('please enter a valid business type')
