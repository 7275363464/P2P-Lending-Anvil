from ._anvil_designer import borrower_registration_form_5_bankTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class borrower_registration_form_5_bank(borrower_registration_form_5_bankTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['account_name']
      self.drop_down_1.selected_value=user_data['account_type']
      self.text_box_3.text=user_data['account_number']
      self.text_box_4.text=user_data['bank_name']
      self.bank_id.text=user_data['bank_id']
      self.branch_name.text=user_data['account_bank_branch']
      user_data.update()
      
    options = app_tables.fin_borrower_account_type.search()
    options_string = [str(option['borrower_account_type']) for option in options]
    self.drop_down_1.items = options_string
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.accepted_terms = False
    self.button_2.enabled = False

    self.setup_event_handlers()

  def setup_event_handlers(self):
    # Attach event handlers for real-time validation
    self.text_box_1.set_event_handler('change', self.validate_account_name)
    self.text_box_1.set_event_handler('lost_focus', self.validate_account_name)
    self.text_box_3.set_event_handler('change', self.validate_account_number)
    self.text_box_3.set_event_handler('lost_focus', self.validate_account_number)
    self.text_box_4.set_event_handler('change', self.validate_bank_name)
    self.text_box_4.set_event_handler('lost_focus', self.validate_bank_name)
    self.bank_id.set_event_handler('change', self.validate_bank_id)
    self.bank_id.set_event_handler('lost_focus', self.validate_bank_id)
    self.branch_name.set_event_handler('change', self.validate_bank_branch)
    self.branch_name.set_event_handler('lost_focus', self.validate_bank_branch)
    self.check_box_1_copy_2.set_event_handler('change', self.check_terms)

  def validate_account_name(self, **event_args):
    account_name = self.text_box_1.text
    if not account_name or not re.match(r'^[A-Za-z\s]+$', account_name):
      self.text_box_1.role = 'outlined-error'
    else:
      self.text_box_1.role = 'outlined'

  def validate_account_number(self, **event_args):
    account_number = self.text_box_3.text
    if ' ' in account_number or not account_number.isdigit():
      self.text_box_3.role = 'outlined-error'
    else:
      self.text_box_3.role = 'outlined'

  def validate_bank_name(self, **event_args):
    bank_name = self.text_box_4.text
    if not bank_name:
      self.text_box_4.role = 'outlined-error'
    else:
      self.text_box_4.role = 'outlined'

  def validate_bank_id(self, **event_args):
    bank_id = self.bank_id.text
    if not bank_id:
      self.bank_id.role = 'outlined-error'
    else:
      self.bank_id.role = 'outlined'

  def validate_bank_branch(self, **event_args):
    bank_branch = self.branch_name.text
    if not bank_branch:
      self.branch_name.role = 'outlined-error'
    else:
      self.branch_name.role = 'outlined'

  def check_terms(self, **event_args):
    self.accepted_terms = self.check_box_1_copy_2.checked
    self.button_2.enabled = self.accepted_terms

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    bank_id = self.bank_id.text
    bank_branch = self.branch_name.text
    account_name = self.text_box_1.text
    account_type = self.drop_down_1.selected_value
    account_number = self.text_box_3.text
    bank_name = self.text_box_4.text
    t_and_c = self.check_box_1_copy_2 
    user_id = self.userId
    
    if not account_name:
      Notification("Please fill in the Account Name").show()
      self.text_box_1.focus()
    elif not account_type:
      Notification("Please select the Account Type").show()
      self.drop_down_1.focus()
    elif not account_number:
      Notification("Please fill in the Account Number").show()
      self.text_box_3.focus()
    elif not bank_name:
      Notification("Please fill in the Bank Name").show()
      self.text_box_4.focus()
    elif not bank_id:
      Notification("Please fill in the Bank ID").show()
      self.bank_id.focus()
    elif not bank_branch:
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
      self.text_box_3.focus()
    elif not account_number.isdigit():
      Notification("Account number should be valid").show()
      self.text_box_3.focus()
    else:
      anvil.server.call('add_borrower_step5', account_name, account_type, account_number, bank_name, user_id)
      anvil.server.call('add_borrower_step6', bank_id, bank_branch, user_id)
      open_form('borrower.dashboard')

  def button_1_click(self, **event_args):
    open_form('borrower.borrower_registration_forms.borrower_registration_form_4_loan',user_id=self.userId)

  def button_3_click(self, **event_args):
    open_form("bank_users.main_form.investNow_applyForLoan")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('Agreements, Privacy Policy and Applicant should accept following:Please note that any information concealed (as what we ask for), would be construed as illegitimate action on your part and an intentional attempt to hide material information which if found in future, would attract necessary action (s) at your sole cost. Hence, request to be truthful to your best knowledge while sharing your details)')

  def check_box_1_copy_2_change(self, **event_args):
        """This method is called when the check box is checked or unchecked"""
        self.accepted_terms = self.check_box_1_copy_2.checked
        self.button_2.enabled = self.accepted_terms