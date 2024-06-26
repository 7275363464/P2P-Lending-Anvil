from ._anvil_designer import RowTemplate58Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate58(RowTemplate58Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    selected_row = self.item
    open_form('admin.dashboard.accounting.payment_receipt.emi_details.payment_receipts', selected_row=selected_row)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    selected_row = self.item
    open_form('admin.dashboard.accounting.payment_receipt.emi_details.payment_receipts', selected_row=selected_row)
