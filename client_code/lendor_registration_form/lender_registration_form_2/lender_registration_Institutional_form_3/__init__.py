from ._anvil_designer import lender_registration_Institutional_form_3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_Institutional_form_3(lender_registration_Institutional_form_3Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = anvil.server.call('get_user_data', user_id)
        
    if user_data:
            self.industry_type = user_data.get('industry_type', '')
            self.turn_over = user_data.get('six_month_turnover', '')
    
    else:
        self.industry_type = ''
        self.turn_over = ''
       
       #Restore previously entered data if available
    if self.industry_type:
            self.text_box_1.text= self.industry_type
    if self.turn_over:
            self.text_box_2.text= self.turn_over
    
    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    industry_type = self.text_box_1.text
    turn_over = self.text_box_2.text
    last_six_statements = self.file_loader_1.file
    user_id = self.userId
    if not industry_type or not turn_over or not last_six_statements:
      Notification("Please fill all the fields").show()
    else:
     anvil.server.call('add_lendor_institutional_form_3',industry_type,turn_over,last_six_statements,user_id)
     open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_5',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_2',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.file_loader_1.file
    
