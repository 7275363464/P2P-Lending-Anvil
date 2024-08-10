from ._anvil_designer import lender_registration_form_1_education_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_1_education_form(lender_registration_form_1_education_formTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.drop_down_1.selected_value = user_data['qualification']
      user_data.update()
    
    
    options = app_tables.fin_lendor_qualification.search()
    options_string = [str(option['lendor_qualification']) for option in options]
    self.drop_down_1.items = options_string
    self.drop_down_1.selected_value = None

    # Initialize all column panels to be invisible initially
    self.column_panel_1.visible = False
    self.column_panel_2.visible = False
    self.column_panel_3.visible = False
    self.column_panel_4.visible = False
    self.column_panel_5.visible = False
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

  def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        qualification = self.drop_down_1.selected_value
        user_id = self.userId

        # Get the uploaded files
        tenth_class = self.file_loader_1.file #,self.file_loader_2.file]
        tenth_class_1 = self.file_loader_2.file
        tenth_class_2 = self.file_loader_4.file
        tenth_class_3 = self.file_loader_7.file
        tenth_class_4 = self.file_loader_11.file
        intermediate = self.file_loader_3.file
        intermediate_1 = self.file_loader_5.file 
        intermediate_2 = self.file_loader_8.file
        intermediate_3 = self.file_loader_12.file
        btech = self.file_loader_6.file
        btech_1 = self.file_loader_9.file
        btech_2 = self.file_loader_13.file 
        mtech = self.file_loader_10.file
        mtech_1 = self.file_loader_14.file
        phd = self.file_loader_15.file
      
        # Validate files based on qualification
        if qualification == '10th standard' and not tenth_class:
            self.file_loader_1.background='#FF0000'
            self.file_loader_1.focus()
            Notification('Please upload All document before proceeding.').show()
            return
        if qualification == '12th standard' and (not tenth_class_1 or not intermediate):
            if not tenth_class_1:
              self.file_loader_2.background = '#FF0000'
              self.file_loader_2.focus()
            if not intermediate:
              self.file_loader_3.background = '#FF0000'
              self.file_loader_3.focus()
            Notification('Please upload All documents before proceeding.').show()
            return
        elif qualification == "Bachelor's degree" and (not tenth_class_2 or not intermediate_1 or not btech):
            if not tenth_class_2:
              self.file_loader_4.background = '#FF0000'
              self.file_loader_4.focus()
            if not intermediate_1:
              self.file_loader_5.background = '#FF0000'
              self.file_loader_5.focus()
            if not btech:
              self.file_loader_6.background = '#FF0000'
              self.file_loader_6.focus()
            Notification("Please upload All documents before proceeding.").show()
            return
        elif qualification == "Master's degree" and (not tenth_class_3 or not intermediate_2 or not btech_1 or not mtech):
            if not tenth_class_3:
              self.file_loader_7.background = '#FF0000'
              self.file_loader_7.focus()
            if not intermediate_2:
              self.file_loader_8.background = '#FF0000'
              self.file_loader_8.focus()
            if not btech_1:
              self.file_loader_9.background = '#FF0000'
              self.file_loader_9.focus()
            if not mtech:
              self.file_loader_10.background = '#FF0000'
              self.file_loader_10.focus()
            Notification("Please upload All documents before proceeding.").show()
            return
        elif qualification == 'PhD' and (not tenth_class_4 or not intermediate_3 or not btech_2 or not mtech_1 or not phd):
            if not tenth_class_4:
              self.file_loader_11.background = '#FF0000'
              self.file_loader_11.focus()
            if not intermediate_3:
              self.file_loader_12.background = '#FF0000'
              self.file_loader_12.focus()
            if not btech_2:
              self.file_loader_13.background = '#FF0000'
              self.file_loader_13.focus()
            if not mtech_1:
              self.file_loader_14.background = '#FF0000'
              self.file_loader_14.focus()
            if not phd:
              self.file_loader_15.background = '#FF0000'
              self.file_loader_15.focus()
            Notification('Please upload all documents before proceeding.').show()
            return
        # Proceed with server call and form navigation
        if qualification == '10th standard':
            anvil.server.call('add_education_tenth', tenth_class, user_id)
        elif qualification == '12th standard':
            anvil.server.call('add_education_int', tenth_class_1, intermediate, user_id)
        elif qualification == "Bachelor's degree":
            anvil.server.call('add_education_btech', tenth_class_2, intermediate_1, btech, user_id)
        elif qualification == "Master's degree":
            anvil.server.call('add_education_mtech', tenth_class_3, intermediate_2, btech_1, mtech, user_id)
        elif qualification == 'PhD':
            anvil.server.call('add_education_phd', tenth_class_4, intermediate_3, btech_2, mtech_1, phd, user_id)
        else:
            self.drop_down_1.role= 'outlined-error'
            self.drop_down_1.focus()
            Notification("Please select a valid qualification status").show()
            return

        open_form('lendor.lendor_registration_forms.lender_registration_form_2', user_id=user_id)

        if qualification not in ['10th standard', '12th standard', "Bachelor's degree", "Master's degree", 'PhD']:
           Notification("Please select a valid qualification status").show()
        elif not user_id:
            Notification("User ID is missing").show()
        else:
          anvil.server.call('add_lender_step1', qualification, user_id)


  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.main_form.investNow_applyForLoan")

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    qualification = self.drop_down_1.selected_value
    # Hide all column panels first
    self.column_panel_1.visible = False
    self.column_panel_2.visible = False
    self.column_panel_3.visible = False
    self.column_panel_4.visible = False
    self.column_panel_5.visible = False
    
    # Show the appropriate column panel based on the selected qualification
    if qualification == '10th standard':
        self.column_panel_1.visible = True
    elif qualification == '12th standard':
        self.column_panel_2.visible = True
    elif qualification == "Bachelor's degree":
        self.column_panel_3.visible = True
    elif qualification == "Master's degree":
        self.column_panel_4.visible = True
    elif qualification == 'PhD':
        self.column_panel_5.visible = True

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.file_name.text = file.name if file else ''
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

      
  def file_loader_2_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_23.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_2.source = self.file_loader_2.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_2.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_2.clear()
      
  def file_loader_3_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_24.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_3.source = self.file_loader_3.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_3.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_3.clear()
      
  def file_loader_4_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_25.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_4.source = self.file_loader_4.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_4.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_4.clear()
      
  def file_loader_6_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_27.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_6.source = self.file_loader_6.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_6.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_6.clear()
      
  def file_loader_7_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_28.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_7.source = self.file_loader_7.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_7.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_7.clear()
      
  def file_loader_8_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_29.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_8.source = self.file_loader_8.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_8.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_8.clear()
      
  def file_loader_9_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_30.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_9.source = self.file_loader_9.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_9.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_9.clear()
      
  def file_loader_10_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_31.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_10.source = self.file_loader_10.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_10.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_10.clear()
      
  def file_loader_11_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_32.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_11.source = self.file_loader_11.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_11.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_11.clear()
  def file_loader_12_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_33.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_12.source = self.file_loader_12.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_12.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_12.clear()
      
  def file_loader_13_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_34.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_13.source = self.file_loader_13.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_13.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_13.clear()
  def file_loader_14_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_35.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_14.source = self.file_loader_14.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_14.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_14.clear()
      
  def file_loader_15_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_36.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_15.source = self.file_loader_15.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_15.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_15.clear()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.basic_registration_form')

  def file_loader_5_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
            self.label_26.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_5.source = self.file_loader_5.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_5.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.file_loader_5.clear()
  
   