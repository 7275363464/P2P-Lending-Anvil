from ._anvil_designer import default_loansTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class default_loans(default_loansTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.data = app_tables.fin_loan_details.search(loan_updated_status=q.like('default%'))

    self.result = []
    for loan in self.data:
        borrower_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
        lender_profile = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
        if borrower_profile is not None and lender_profile is not None:
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
                'lender_mobile': lender_profile['mobile']  ,
                'product_name':loan['product_name'],
                'product_description':loan['product_description'],
                'loan_disbursed_timestamp':loan['loan_disbursed_timestamp'],
                'borrower_photo':borrower_profile['user_photo'],
                'lender_photo':lender_profile['user_photo']
            })

    if not self.result:
        alert("No Default Loans Available!")
    else:
        panel1_data = self.result[::2]  
        panel2_data = self.result[1::2]
        self.repeating_panel_1.items = panel1_data
        self.repeating_panel_3.items = panel2_data
        # self.repeating_panel_1.items = self.result
  #   # Any code you write here will run before the form opens.
  #   self.loan = tables.app_tables.fin_loan_details.search()
  #   self.fourcloser = tables.app_tables.foreclosure.search()
  #   self.today = datetime.now().date()
  #   print(self.today)

  #   self.due_list = []
  #   self.loan_amont = []
  #   self.paid_amount = []
  #   self.intrest = []
  #   self.loan_due_amount = []

  #   self.id = []
  #   self.c_id = []
  #   self.full_name = []
  #   self.status = []
  #   for i in self.loan:
  #     self.due_list.append(i['due_date'].date())
  #     self.loan_amont.append(i['loan_amount'])
  #     self.id.append(i['loan_id'])
  #     self.intrest.append(i['interest_rate'])
  #     self.loan_due_amount.append(i['total_repayment_amount'])
  #     self.c_id.append(i['borrower_customer_id'])
  #     self.full_name.append(i['borrower_full_name'])
  #     self.status.append(i['loan_updated_status'])


  #   self.index = []  
  #   b = -1
  #   for i in self.id:
  #     b += 1
  #     if (self.loan_due_amount[b] != 0) and (self.status[b] != "closed"):
  #       self.index.append(self.id[b])

  #   print(self.index)
  #   self.result = []
  #   self.days = {}
  #   for i in self.index:
  #     c = self.id.index(i)
  #     print(c)
  #     d = ((self.today - self.due_list[c]).days > 3) and ((self.today - self.due_list[c]).days < 90)
  #     if (self.due_list[c] < self.today) and (d):
  #       annual_interest_rate = self.intrest[c]
  #       days_in_year = 365
  #       daily_interest_rate = (annual_interest_rate / 100) / days_in_year
        
  #       self.result.append(self.id[c])
  #       interest_per_day = self.loan_due_amount[c] * daily_interest_rate
  #       days_late = (self.today - self.due_list[c]).days
  #       penalty = interest_per_day * days_late
  #       total_due = self.loan_due_amount[c] + penalty
  #       self.days[self.id[c]] = total_due
    
    
  #   self.index1 = []
  #   self.final = []
  #   self.total = []
  #   for id, total in self.days.items():
  #     self.index1.append(self.id.index(id))
  #     self.total.append(total)

  #   a = -1
  #   for i in self.index1:
  #     a += 1
  #     self.final.append({'loan_id' : self.id[i], 'coustmer_id' : self.c_id[i], 'full_name' : self.full_name[i], 'amount': int(self.total[a])})

  #   self.repeating_panel_1.items = self.final
  # # def link_1_click(self, **event_args):
  # #   """This method is called when the link is clicked"""
  #   open_form('admin.dashboard.loan_management')

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.loan_management.view_loans')
