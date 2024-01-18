from ._anvil_designer import view_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module
from datetime import datetime

class view_profile(view_profileTemplate):
  def __init__(self, selected_row, **properties):
    self.user_id=main_form_module.userId
    self.init_components(**properties)

    # Display loan details
    self.loan_id_label.text = f"{selected_row['loan_id']}"
    self.loan_amount_label.text=f"{selected_row['credit_limit']}"
    self.intrest_rate_label.text=f"{selected_row['interest_rate']}"
    self.tenure_label.text=f"{selected_row['tenure']}"
    self.date_of_apply_label.text=f"{selected_row['timestamp']}"
    self.due_amount_label.text=f"{selected_row['loan_amount']}"
    self.due_date_label.text=f"{selected_row['due_date']}"
    
    due_date = selected_row['due_date']
    days_left = (due_date-datetime.now()).days
    self.days_left_label.text = f"{days_left} days left"
    
  def button_1_copy_click(self, **event_args):
    open_form('borrower_registration_form.dashboard')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.borrower_today_dues')
