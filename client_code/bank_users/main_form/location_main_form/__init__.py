from ._anvil_designer import location_main_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator


class location_main_form(location_main_formTemplate):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.




  def login_signup_button_click(self, **event_args):
    anvil.users.login_with_form()
    current_user = anvil.users.get_user()
    if current_user:
      user_email = current_user['email']
      print(user_email)
      check_user_already_exist = user_module.check_user_profile(user_email)
      print(check_user_already_exist)
      if check_user_already_exist == None:
        print("main if statement was executed")
        user_module.add_email_and_user_id(user_email)
        main_form_module.email = user_email
        main_form_module.flag = True
        open_form('bank_users.user_form')
      else:
        check_user_registration = user_module.check_user_registration_form_done_or_not_engine(user_email)
        print("main else statement was executed")
        if check_user_registration:
          user_profile_e = app_tables.user_profile.get(email_user=user_email)
          main_form_module.email = user_email
          borrower_main_form_module.userId = user_module.find_user_id(user_email)
          if user_profile_e is not  None:
            user_type = user_profile_e['usertype']
            if user_type == 'lender':
              open_form('lendor_registration_form.dashboard')
            elif user_type == 'borrower':
              open_form('bank_users.borrower_rgistration_form')
            elif user_type == 'admin':
              open_form('admin.dashboard')
              open_form('bank_users.main_form.investNow_applyForLoan')
        else:
          main_form_module.email = user_email
          main_form_module.flag = False
          open_form('bank_users.main_form.investNow_applyForLoan')

#-- imp logic dont go up--#

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form")



  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.about_main_form")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.products_main_form")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.contact_main_form")

  def carrer_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.career_main_form")







    # Replace these coordinates with the desired latitude and longitude




   





