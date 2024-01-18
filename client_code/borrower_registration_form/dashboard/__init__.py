from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from ...bank_users.user_form import user_module

class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    email= main_form_module.email
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.email = main_form_module.email
    email = self.email
    # Any code you write here will run before the form opens.


  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("borrower_registration_form.dashboard")

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Logged out sucessfully")
    anvil.users.logout()
    open_form('bank_users.main_form')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.borrower_profile')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.new_loan_request')

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.view_loans')

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.today_dues')

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.application_tracker')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.foreclosure_request')

  def outlined_button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.discount_coupons')

  def outlined_button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.borrower.view_portfolio')

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower_registration_form.dashboard.dashboard_about')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("borrower_registration_form.dashboard.dashboard_contact")

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor_registration_form.dashboard.notification')

  def wallet_dashboard_link_click(self, **event_args):
    user_profiles = server.call('fetch_user_profiles')
    
    for profile in user_profiles:
        result = server.call(
            'create_wallet_entry',
            profile['email_user'],
            profile['customer_id'],
            profile['full_name'],
            profile['usertype']
        )
        
        print(result)
    
    open_form('wallet.wallet')
    
    customer_id = 1000
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)