from ._anvil_designer import lender_registration_form_4_bank_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class lender_registration_form_4_bank_form_1(lender_registration_form_4_bank_form_1Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.bank_id.text=user_data['bank_id']
      self.branch_name.text=user_data['account_bank_branch']
      self.text_box_1.text=user_data['account_name']
      self.drop_down_1.selected_value=user_data['account_type']
      self.text_box_2.text=user_data['account_number']
      self.text_box_3.text=user_data['bank_name']
      user_data.update()

      
    options = app_tables.fin_lendor_account_type.search()
    options_string =[str(option['lendor_account_type']) for option in options]
    self.drop_down_1.items = options_string
    self.setup_event_handlers()
    self.accepted_terms = False
    self.button_2.enabled = False
    # Any code you write here will run before the form opens.
  def setup_event_handlers(self):
    # Attach event handlers for real-time validation
      self.text_box_1.set_event_handler('change', self.validate_account_name)
      self.text_box_1.set_event_handler('lost_focus', self.validate_account_name)
      self.text_box_2.set_event_handler('change', self.validate_account_number)
      self.text_box_2.set_event_handler('lost_focus', self.validate_account_number)
      self.text_box_3.set_event_handler('change', self.validate_bank_name)
      self.text_box_3.set_event_handler('lost_focus', self.validate_bank_name)
      self.bank_id.set_event_handler('change', self.validate_bank_id)
      self.bank_id.set_event_handler('lost_focus', self.validate_bank_id)
      self.branch_name.set_event_handler('change', self.validate_bank_branch)
      self.branch_name.set_event_handler('lost_focus', self.validate_bank_branch)
      self.check_box_1_copy_3.set_event_handler('change', self.check_terms)

  def validate_account_name(self, **event_args):
    account_name = self.text_box_1.text
    if not account_name or not re.match(r'^[A-Za-z\s]+$', account_name):
      self.text_box_1.background = 'red'
    else:
      self.text_box_1.background = 'white'

  def validate_account_number(self, **event_args):
    account_number = self.text_box_2.text
    if ' ' in account_number or not account_number.isdigit():
      self.text_box_2.background = 'red'
    else:
      self.text_box_2.background = 'white'

  def validate_bank_name(self, **event_args):
    bank_name = self.text_box_3.text
    if not bank_name:
      self.text_box_3.background = 'red'
    else:
      self.text_box_3.background = 'white'

  def validate_bank_id(self, **event_args):
    bank_id = self.bank_id.text
    if not bank_id:
      self.bank_id.background = 'red'
    else:
      self.bank_id.background = 'white'

  def validate_bank_branch(self, **event_args):
    branch_name = self.branch_name.text
    if not branch_name:
      self.branch_name.background = 'red'
    else:
      self.branch_name.background = 'white'

  def check_terms(self, **event_args):
    self.accepted_terms = self.check_box_1_copy_3.checked
    self.button_2.enabled = self.accepted_terms
  
  def button_2_click(self, **event_args):
    bank_id = self.bank_id.text
    branch_name = self.branch_name.text
    account_name = self.text_box_1.text
    account_type = self.drop_down_1.selected_value
    account_number = self.text_box_2.text
    bank_name = self.text_box_3.text
    t_and_c = self.check_box_1_copy_3 
    
    user_id = self.userId
    if not account_name:
      Notification("Please fill in the Account Name").show()
      self.text_box_1.focus()
    elif not account_type:
      Notification("Please select the Account Type").show()
      self.drop_down_1.focus()
    elif not account_number:
      Notification("Please fill in the Account Number").show()
      self.text_box_2.focus()
    elif not bank_name:
      Notification("Please fill in the Bank Name").show()
      self.text_box_3.focus()
    elif not bank_id:
      Notification("Please fill in the Bank ID").show()
      self.bank_id.focus()
    elif not branch_name:
      Notification("Please fill in the Branch Name").show()
      self.branch_name.focus()
    elif not t_and_c:
      Notification("Please accept the terms and conditions").show()
      self.check_box_1_copy_3.focus()
    elif not re.match(r'^[A-Za-z\s]+$', account_name):
      Notification("Account name should be valid").show()
      self.text_box_1.focus()
    elif ' ' in account_number:
      Notification("Account number should not contain spaces").show()
      self.text_box_2.focus()
    elif not account_number.isdigit():
      Notification("Account number should be valid").show()
      self.text_box_2.focus()
    else:
      anvil.server.call('add_lendor_bank_details_form_2', bank_id, branch_name, user_id)
      anvil.server.call('add_lendor_bank_details_form_1', account_name, account_type, account_number, bank_name, user_id)
      open_form('lendor.dashboard')

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=self.userId)

  # def button_3_click(self, **event_args):
  #   open_form("bank_users.user_form")

  def link_1_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('Agreements, Privacy Policy and Applicant should accept following:Please note that any information concealed (as what we ask for), would be construed as illegitimate action on your part and an intentional attempt to hide material information which if found in future, would attract necessary action (s) at your sole cost. Hence, request to be truthful to your best knowledge while sharing your details)')

  def check_box_1_copy_3_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.accepted_terms = self.check_box_1_copy_3.checked
    self.button_2.enabled = self.accepted_terms
    
