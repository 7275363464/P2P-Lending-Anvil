from ._anvil_designer import under_processTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class under_process(under_processTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.data = app_tables.fin_loan_details.search(loan_updated_status=q.like('under process%'))

    self.result = []
    for loan in self.data:
        borrower_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
        # lender_profile = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
        if borrower_profile is not None :
            self.result.append({
                'loan_id': loan['loan_id'],
                'customer_id': loan['borrower_customer_id'],
                'full_name': loan['borrower_full_name'],
                'loan_status': loan['loan_updated_status'],
                'lender_full_name': loan['lender_full_name'],
                'borrower_full_name': loan['borrower_full_name'],
                'lender_customer_id': loan['lender_customer_id'],
                'interest_rate': loan['interest_rate'],
                'tenure': loan['tenure'],
                'loan_amount': loan['loan_amount'],
                'lender_timestamp': loan['lender_accepted_timestamp'],
                'borrower_mobile': borrower_profile['mobile'],  # Include additional profile details here
                # 'lender_mobile': lender_profile['mobile']  ,
                'product_name':loan['product_name'],
                'product_description':loan['product_description'],
                'loan_disbursed_timestamp':loan['loan_disbursed_timestamp'],
                'borrower_photo':borrower_profile['user_photo'],
                # 'lender_photo':lender_profile['user_photo']
            })

    if not self.result:
        alert("No under process Loans Available!")
    else:
        panel1_data = self.result[::2]  
        panel2_data = self.result[1::2]
        self.repeating_panel_2.items = panel1_data
        self.repeating_panel_3.items = panel2_data

  # def link_1_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form('admin.dashboard.loan_management')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.dashboard.performance_tracker')

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.loan_management.view_loans')
