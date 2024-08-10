from ._anvil_designer import wallet_depositTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form, server
# from .. import bmain_form_module as main_form_module
# from ...lendor_registration_form.dashboard import lendor_main_form_module as main_form_module
from ...borrower.dashboard import main_form_module
from datetime import datetime, timezone
from datetime import timedelta
import time
from ...lendor.dashboard.Module1 import transfer_money

class wallet_deposit(wallet_depositTemplate):
  def __init__(self,entered_loan_id,entered_borrower_customer_id,time_difference_seconds, **properties):
    self.entered_loan_id = entered_loan_id
    self.entered_borrower_customer_id = entered_borrower_customer_id
    self.time_difference_seconds = time_difference_seconds
    self.user_id = main_form_module.userId
    self.selected_row = None
    # self.selected_row = selected_row
    self.start_time = time.time()
    start_time = self.start_time
    
    self.check_time_difference()

    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.deposit_placeholder = "5000"
    # self.withdraw_placeholder = "0.00"

    self.email=main_form_module.email
    email = self.email


    wallet_row =app_tables.fin_wallet.get(user_email=email)
    if wallet_row:
      self.balance_lable.text = wallet_row['wallet_amount']

    # self.user_id = main_form_module.userId
    # user_id = self.user_id

    # self.user_id = main_form_module.userId
    # user_id = self.user_id
  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user_request = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_request:
      self.user_type = user_request['usertype']

    if self.user_type == "lender":
      open_form("lendor.dashboard")
    else:
      open_form("borrower.dashboard")


  # def about_main_form_link_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form("lendor_registration_form.dashboard.dasboard_about")

  # def contact_main_form_link_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form("lendor_registration_form.dashboard.dasboard_contact")

  # def notification_link_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form('lendor_registration_form.dashboard.notification')

  # def button_2_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   pass

  # def deposit_btn_click(self, **event_args):
  #   """This method is called when the button is clicked"""

  #   self.amount_text_box.placeholder = self.deposit_placeholder
  #   self.deposit_money_btn.visible = True
  #   self.withdraw_money_btn.visible = False


  def withdraw_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.amount_text_box.placeholder = self.withdraw_placeholder
    self.deposit_money_btn.visible = False
    self.withdraw_money_btn.visible = True
    self.deposit_btn.visible = True

  def wallet_dashboard_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
          
  def deposit_money_btn_click(self, **event_args):
    amount_entered = self.amount_text_box.text

    # Check if amount_entered is not empty and is a valid number
    if not amount_entered or not str(amount_entered).isdigit():
        alert("Please enter a valid amount.")
        return

    try:
        deposit_amount = int(amount_entered)
    except ValueError:
        alert("Please enter a valid amount.")
        return

    customer_id = self.user_id
    email = self.email
    selected_row = self.selected_row

    if anvil.server.call('deposit_money', email=email, deposit_amount=deposit_amount, customer_id=customer_id):
        alert("Deposit successful!")

        # Update the balance label with the new balance value
        wallet_row = app_tables.fin_wallet.get(user_email=email)
        if wallet_row:
            wallet_amount = wallet_row['wallet_amount']

            # Update the balance label
            self.balance_lable.text = f"Balance: {wallet_amount}"

            entered_loan_id = self.entered_loan_id
            loan_row = app_tables.fin_loan_details.get(loan_id=entered_loan_id)

            if loan_row:
                # Get the loan_amount and subtract it from the wallet_amount
                loan_amount = loan_row['loan_amount']
                alert(f"Loan amount: {loan_amount}")

                # Check if wallet_amount is sufficient for the loan
                if wallet_amount >= loan_amount:
                    # Make the loan_disbursment_btn visible
                    self.loan_disbursment_btn.visible = True
                else:
                    alert("Wallet amount is insufficient. Deposit enough amount.")
                    # Hide the loan_disbursment_btn
                    self.loan_disbursment_btn.visible = False
            else:
                alert("Loan details not found.")
    else:
        alert("Deposit failed!")
          
  def check_time_difference(self):
        current_time = datetime.now(timezone.utc)
        # print("current_time:", current_time)
        start_time_utc = datetime.utcfromtimestamp(self.start_time).replace(tzinfo=timezone.utc)
        
        time_difference = current_time - start_time_utc
        time_diff = 1800 - self.time_difference_seconds 

        if time_difference.total_seconds() > time_diff:  # 1800 seconds = 30 minutes
            # Update loan status based on the comparison of wallet_amount and loan_amount
            
            wallet_row = app_tables.fin_wallet.get(user_email=self.email)
            loan_row = app_tables.fin_loan_details.get(loan_id=self.entered_loan_id)

            if wallet_row and loan_row:
                loan_amount = loan_row['loan_amount']
                lender_accepted_timestamp = loan_row['lender_accepted_timestamp']
                wallet_amount = wallet_row['wallet_amount']
                entered_loan_id = self.entered_loan_id 
                entered_borrower_customer_id = self.entered_borrower_customer_id

                if loan_amount > wallet_amount:
                    # Update loan status to 'lost opportunities'
                    loan_row['loan_updated_status'] = 'lost opportunities'
                    loan_row.update()
                    print("loan_updated_status as lost opportunities")
                    alert("The designated time has passed. The loan has moved to the 'Lost Opportunities' status.")
                    open_form('lendor.dashboard')
                else:
                    alert("Time has passed, but wallet_amount is sufficient. No change in loan status.")
                    open_form('lendor.dashboard')
            else:
                alert("Error: Wallet or loan details not found.")

   
  def form_show(self, **event_args):
        self.start_time = time.time()  # Set the start time when the form is shown
        self.check_time_difference()
    
  def loan_disbursment_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    customer_id = self.user_id
    email = self.email
    entered_loan_id = self.entered_loan_id 
    entered_borrower_customer_id = self.entered_borrower_customer_id
    loan_deta = app_tables.fin_loan_details.get(loan_id=entered_loan_id)
    if loan_deta is not None:
        self.lender_customer_id = loan_deta['lender_customer_id']
        print("lender", self.lender_customer_id)
    wallet_row = app_tables.fin_wallet.get(user_email=email)
    if wallet_row:
      entered_loan_id = self.entered_loan_id
      loan_row = app_tables.fin_loan_details.get(loan_id=entered_loan_id)
              
      if loan_row:
        # Get the loan_amount and subtract it from the wallet_amount
        loan_amount = loan_row['loan_amount']
        loan_updated_status = loan_row["loan_updated_status"]
        loan_disbursed_timestamp = loan_row["loan_disbursed_timestamp"]
        new_balance = wallet_row['wallet_amount'] - loan_amount

        # Update the wallet_amount in fin_wallet
        wallet_row['wallet_amount'] = new_balance
        wallet_row.update()
        
        # Update the balance label with the new balance value
        self.balance_lable.text = f"{new_balance}"

        if loan_disbursed_timestamp is not None:
          # Update the loan_disbursed_timestamp with the current datetime
          loan_row['loan_disbursed_timestamp'] = datetime.now()
        else:
          # Set the loan_disbursed_timestamp for the first time if it is None
          loan_row['loan_disbursed_timestamp'] = datetime.now()

        # Calculate and set the first EMI payment due date (only date portion)
        emi_payment_type = loan_row['emi_payment_type']
        loan_disbursed_timestamp = loan_row['loan_disbursed_timestamp']
        tenure = loan_row['tenure']
        first_emi_due_date = self.calculate_first_emi_due_date(emi_payment_type, loan_disbursed_timestamp, tenure)

        loan_row['first_emi_payment_due_date'] = first_emi_due_date

        entered_borrower_customer_id = self.entered_borrower_customer_id
        # Convert entered_borrower_customer_id to integer
        try:
            entered_borrower_customer_id = int(entered_borrower_customer_id)
        except ValueError:
            alert("Please enter a valid customer ID.")
            return
          
        wallet_add = app_tables.fin_wallet.get(customer_id=entered_borrower_customer_id)
        if wallet_add:
          loan_amount = loan_row['loan_amount']
          
          if wallet_add['wallet_amount'] is None:
            wallet_add['wallet_amount'] = 0
            
          wallet_add['wallet_amount'] += loan_amount
          wallet_add.update()
          transfer_money(lender_id = self.lender_customer_id, borrower_id=entered_borrower_customer_id, transfer_amount=loan_amount)
          # You may want to update the loan_updated_status here if needed
          updated_loan_status = 'disbursed'
          loan_row['loan_updated_status'] = updated_loan_status
          # Save the changes to the loan_row
          loan_row.update()
          
          self.check_time_difference()
                  
          alert(f"Loan Amount Paid to Borrower\nWallet Amount Updated")
          open_form('lendor.dashboard')
          return
        else:
            alert("Wallet not found for the entered borrower customer ID.") 
      else:
        alert("Loan details not found.")
    else:
      alert("Wallet not found for the entered lender customer ID.") 
    
  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.check_time_difference()
    # Print time_difference every 300 seconds i.e 5min
    if int(time.time() - self.start_time) % 300 == 0:
      print("time_difference:", datetime.now(timezone.utc) - datetime.utcfromtimestamp(self.start_time).replace(tzinfo=timezone.utc))
  
  def calculate_first_emi_due_date(self, emi_payment_type, loan_disbursed_timestamp, tenure):
        if emi_payment_type == "Monthly":
            first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=30)).date()
        elif emi_payment_type == "Three Months":
            first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=90)).date()
        elif emi_payment_type == "Six Months":
            first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=180)).date()
        elif emi_payment_type == "One Time":
            if tenure:
                # Add the tenure in months to the loan_disbursed_timestamp
                first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=30 * tenure)).date()
            else:
                # Handle the case where tenure is not provided (raise an exception or set to None)
                first_emi_due_date = None
        else:
            # Handle other cases or raise an exception as needed
            first_emi_due_date = None

        return first_emi_due_date

  def all_transaction_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("wallet.wallet.all_transaction")
