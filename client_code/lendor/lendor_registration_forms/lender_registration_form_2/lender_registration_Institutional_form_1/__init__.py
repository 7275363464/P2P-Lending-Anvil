from ._anvil_designer import lender_registration_Institutional_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re


class lender_registration_Institutional_form_1(lender_registration_Institutional_form_1Template):

  business_name_is_valid = False
  business_add_is_valid = False
  business_type_is_valid = False
  year_estd_is_valid = False
  industry_type_is_valid = False
  six_month_turn_over_is_valid = False
  cin_is_valid = False
  din_is_valid = False
  registered_off_add_is_valid = False
  lendor_business_type_is_valid = False  
  employees_working_is_valid = False
  
  def __init__(self, user_id,**properties):
        self.userId = user_id
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
                
        user_data=app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
              self.text_box_1_copy.text = user_data['business_add']
              self.text_box_2_copy.text = user_data['business_name']
              self.drop_down_12.selected_value = user_data['business_type']
              self.date_picker_1.date = user_data['year_estd']
              self.text_box_3.text = user_data['industry_type']
              self.text_box_4.text = user_data['six_month_turnover']      
              self.drop_down_4.selected_value = user_data['employees_working']
              self.text_box_5.text = user_data['din'] 
              self.text_box_6.text = user_data['cin']
              self.text_box_7.text = user_data['registered_off_add']
        
        
              options = app_tables.fin_lendor_business_type.search()
              options_string = [str(option['lendor_business_type']) for option in options]
              self.drop_down_12.items = options_string

              self.text_box_1_copy.add_event_handler('change', self.validate_business_add)
              self.text_box_2_copy.add_event_handler('change', self.validate_business_name)
              self.date_picker_1.add_event_handler('change', self.validate_year_estd)
              self.text_box_3.add_event_handler('change', self.validate_industry_type)
              self.text_box_4.add_event_handler('change', self.validate_six_month_turnover)
              self.text_box_5.add_event_handler('change', self.validate_din)
              self.text_box_6.add_event_handler('change', self.validate_cin)
              self.text_box_7.add_event_handler('change', self.validate_registered_off_add)
              self.drop_down_4.add_event_handler('change', self.validate_no_of_employes)
              self.drop_down_12.add_event_handler('change', self.validate_business_type)
              self.file_loader_1.add_event_handler('change', self.validate_file_upload)
              self.file_loader_1_copy.add_event_handler('change', self.validate_file_upload)

        
        
  def validate_business_add(self, **event_args):
        Business_add = self.text_box_1_copy.text
        global business_add_is_valid
        if re.match(r'^[A-Za-z\d][A-Za-z\d\s]*$', Business_add):
            self.text_box_1_copy.role = 'outlined'
            business_add_is_valid = True
        else:
            self.text_box_1_copy.role = 'outlined-error'
            business_add_is_valid = False
            alert('please enter a valid business address')

  def validate_business_name(self, **event_args):
        global business_name_is_valid
        business_name = self.text_box_2_copy.text        
        if re.match(r'^[A-Za-z][A-Za-z\s]*$', business_name):
            self.text_box_2_copy.role = 'outlined'            
            business_name_is_valid = True
        else:
            self.text_box_2_copy.role = 'outlined-error'
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
    
  
  # def validate_din(self, **event_args):
  #       din = self.text_box_5.text
  #       global din_is_valid
  #       if re.match(r'^\d+$', din):
  #           self.text_box_5.role = 'outlined'
  #           din_is_valid = True
  #       elif ' ' in din:
  #           alert('Spaces are not valid in din')
  #       else:
  #           self.text_box_5.role = 'outlined-error'
  #           din_is_valid = False
  #           alert("enter a valid din number")
            

  # def validate_cin(self, **event_args):
  #       cin = self.text_box_6.text
  #       global cin_is_valid
  #       if re.match(r'^\d+$', cin):
  #           self.text_box_6.role = 'outlined'   
  #           cin_is_valid = True
  #       elif ' 'in cin:
  #           alert('Spaces are not allowed in cin')
  #       else:
  #           self.text_box_6.role = 'outlined-error'
  #           cin_is_valid = False
  #           alert('please enter a valid cin number')

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

  def validate_business_type(self, **event_args):
        Business_type = self.drop_down_12.selected_value
        global business_type_is_valid
        if Business_type is not None:
            self.drop_down_12.role = 'outlined'
            business_type_is_valid = True
        else:
            self.drop_down_12.role = 'outlined-error'
            business_type_is_valid = False
            alert('please enter a valid business address')

  def validate_no_of_employes(self, **event_args):
        No_of_employes = self.drop_down_4.selected_value
        global business_type_is_valid
        if No_of_employes is not None:
            self.drop_down_4.role = 'outlined'
            business_type_is_valid = True
        else:
            self.drop_down_4.role = 'outlined-error'
            business_type_is_valid = False
            alert('please enter a valid business address')
          
  def button_2_click(self, **event_args):
      self.validate_business_name()
      self.validate_business_add()
      self.validate_industry_type()
      self.validate_six_month_turnover()
      self.validate_cin()
      self.validate_din()
      self.validate_registered_off_add()
      business_name = self.text_box_2_copy.text
      business_add = self.text_box_1_copy.text
      business_type = self.drop_down_12.selected_value        
      empolyees_working = self.drop_down_4.selected_value
      year = self.date_picker_1.date
      industry_type = self.text_box_3.text
      turn_over = self.text_box_4.text
      last_six_statements = self.file_loader_1.file
      din = self.text_box_5.text
      cin = self.text_box_6.text
      reg_off_add = self.text_box_7.text
      proof_verification = self.file_loader_1_copy.file
      global business_type_is_valid
      global employees_working_is_valid

      # if not user_photo:
      #       self.registration_img_file_loader.role = 'outlined-error'
      #       self.registration_img_file_loader.focus()
      #       Notification('Please fill all details').show()
      #       return
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

      if not last_six_statements:
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
        
      user_id = self.userId 
      global business_name_is_valid
      global business_add_is_valid
      global industry_type_is_valid
      global six_month_turn_over_is_valid
      global din_is_valid
      global cin_is_valid
      global registered_off_add_is_valid
      if business_name_is_valid and business_add_is_valid and industry_type_is_valid and six_month_turn_over_is_valid and din_is_valid and cin_is_valid and registered_off_add_is_valid and business_type_is_valid and employees_working_is_valid:
        anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
        months = (datetime.now().year - year.year) * 12 + (datetime.now().month - year.month)
        anvil.server.call('add_lendor_institutional_form_2', year, months, industry_type, turn_over, last_six_statements, user_id)
        anvil.server.call('add_lendor_institutional_form_3', din, cin, reg_off_add, proof_verification, user_id)
        open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=user_id)
      else :
          alert('please fill all the details')
      # Validation for Business
      # if not re.match(r'^[A-Za-z\s]+$', business_name):
      #   alert('Enter valid business name')
      # elif not business_name or not business_add or not business_type or not empolyees_working:
      #   Notification("Please fill all the fields").show()
  
      # elif year and year.year > today.year:
      #   alert("The year cannot be in the future. Please select a valid year.", title="Invalid Year")
      #   return
      # elif year and year.year == today.year and year.month > today.month:
      #   alert("The month cannot be in the future. Please select a valid month.", title="Invalid Month")
      #   return
      # elif year and year.year == today.year and year.month == today.month and year.day > today.day:
      #   alert("The date cannot be in the future. Please select a valid date.", title="Invalid Date")
      #   return              
      # elif not year or not industry_type or not turn_over or not last_six_statements:
      #   alert("Please fill all the fields", title="Missing Information")
      # elif ' ' in cin:
      #   Notification("Spaces are not allowed in the CIN input").show()
      #   return    
      # # DIN Validation
      # elif ' ' in din:
      #   Notification("Spaces are not allowed in the DIN input").show()
      #   return
      # Other field validations
      # elif not din or not cin or not reg_off_add or not proof_verification:
      #   Notification("Please fill all the fields").show()
      # else:
      #   anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
      #   months = (datetime.now().year - year.year) * 12 + (datetime.now().month - year.month)
      #   anvil.server.call('add_lendor_institutional_form_2', year, months, industry_type, turn_over, last_six_statements, user_id)
      #   anvil.server.call('add_lendor_institutional_form_3', din, cin, reg_off_add, proof_verification, user_id)
      #   open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=user_id)

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
              
  def file_loader_1(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
                self.label_3.text = file.name if file else ''
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

  def file_loader_1_copy(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
                  self.label_1.text = file.name if file else ''
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

  def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("bank_users.user_form")
    
  def button_1_click(self, **event_args):
        user_id = self.userId
        open_form('lendor.lendor_registration_forms.lender_registration_form_2',user_id = user_id)
        """This method is called when the button is clicked"""

    



 