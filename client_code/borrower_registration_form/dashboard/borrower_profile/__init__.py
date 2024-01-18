from ._anvil_designer import borrower_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class borrower_profile(borrower_profileTemplate):
  def __init__(self, **properties):
    self.user_id=main_form_module.userId
    #self.user_id=1000
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    user_profile=app_tables.user_profile.get(customer_id=self.user_id)
    if user_profile: 
      
      self.full_name_label.text=user_profile['full_name']
      self.email_id_label.text=user_profile['email_user']
      self.mobile_no_label.text=user_profile['mobile']
      self.date_of_birth_label.text=user_profile['date_of_birth']
      self.city_label.text=user_profile['city']
      self.pan_no_label.text=user_profile['pan_number']
      self.aadhaar_no_label.text=user_profile['aadhaar_no']
      self.gender_label.text=user_profile['gender']
      self.mother_tounge_label.text=user_profile['mouther_tounge']
      self.marrital_status_label.text=user_profile['marital_status']
      self.user_type_label.text=user_profile['usertype']
  def button_1_click(self, **event_args):
    open_form('bank_users.borrower_d.boorrower_edit_profile')

  def button_1_copy_click(self, **event_args):
    open_form('borrower_registration_form.dashboard')
