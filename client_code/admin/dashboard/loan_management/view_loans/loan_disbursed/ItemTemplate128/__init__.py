from ._anvil_designer import ItemTemplate128Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate128(ItemTemplate128Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def outlined_button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        value_to_pass = self.loan_id.text
        open_form('admin.dashboard.loan_management.view_loans.loan_disbursed.view_profile_6', value_to_pass)
        
