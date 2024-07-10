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

    # Any code you write here will run before the form opens.

  def borrower_dashboard_home_linkhome_borrower_registration_button_copy_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.investNow_applyForLoan')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.borrower_registration_forms.dashboard_contact_copy')

  def About_Us_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.borrower_registration_forms.dashboard_about_borrower_registration_form')

  def Report_A_Problem_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.borrower_registration_forms.dashboard_report_a_problem_copy')
