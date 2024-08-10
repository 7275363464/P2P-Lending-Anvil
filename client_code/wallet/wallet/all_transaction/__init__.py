from ._anvil_designer import all_transactionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class all_transaction(all_transactionTemplate):
  def __init__(self, **properties):
    self.user_id = main_form_module.userId
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.repeating_panel_1.items = app_tables.fin_wallet_transactions.search()
    self.repeating_panel_1.items = app_tables.fin_wallet_transactions.search(
    customer_id=self.user_id)
    # Any code you write here will run before the form opens.

  

  def back_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("wallet.wallet")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user_request = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_request:
      self.user_type = user_request['usertype']

    if self.user_type == "lender":
      open_form("lendor.dashboard.dasboard_about")
    else:
      open_form("borrower.dashboard.dashboard_about")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user_request = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_request:
      self.user_type = user_request['usertype']

    if self.user_type == "lender":
      open_form("lendor.dashboard.dasboard_contact")
    else:
      open_form("borrower.dashboard.dashboard_contact")

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user_request = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_request:
      self.user_type = user_request['usertype']

    if self.user_type == "lender":
      open_form('lendor.dashboard.notification')
    else:
      open_form('borrower.dashboard.notification')

  def wallet_dashboard_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wallet.wallet')

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user_request = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_request:
      self.user_type = user_request['usertype']

    if self.user_type == "lender":
        open_form("lendor.dashboard")
    else:
        open_form("borrower.dashboard")
