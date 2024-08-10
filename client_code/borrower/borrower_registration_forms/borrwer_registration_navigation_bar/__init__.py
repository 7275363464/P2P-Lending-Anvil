from ._anvil_designer import borrwer_registration_navigation_barTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class borrwer_registration_navigation_bar(borrwer_registration_navigation_barTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
  def home_main_form_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('bank_users.main_form')

  def about_main_form_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('bank_users.main_form.about_main_form')

  def contact_main_form_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('bank_users.main_form.contact_main_form')  
 