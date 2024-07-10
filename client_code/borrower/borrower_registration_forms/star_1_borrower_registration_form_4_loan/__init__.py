from ._anvil_designer import star_1_borrower_registration_form_4_loanTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_4_loan(star_1_borrower_registration_form_4_loanTemplate):
    def __init__(self, user_id, **properties):
        self.init_components(**properties)
        self.user_id = user_id
        
        self.home_loan_status = ''
        self.other_loan_status = ''
        self.credit_card_loan_status = ''
        self.vehicle_loan_status = ''
        # Initialize interaction flags for the toggle switches
        self.toggleswitch_1_interacted = False
        self.toggleswitch_2_interacted = False
        self.toggleswitch_3_interacted = False
        self.toggleswitch_4_interacted = False
        
        self.load_loan_status()
    
    def load_loan_status(self):
        user_data = app_tables.fin_user_profile.get(customer_id=self.user_id)
        if user_data:
            self.home_loan_status = user_data['home_loan']
            self.other_loan_status = user_data['other_loan']
            self.credit_card_loan_status = user_data['credit_card_loans']
            self.vehicle_loan_status = user_data['vehicle_loan']

    def update_loan_status(self, loan_type, status):
        # Update loan status and save to database
        user_data = app_tables.fin_user_profile.get(customer_id=self.user_id)
        if user_data:
            user_data[loan_type] = status
            user_data.update()
            # Update visibility after status change
            self.load_loan_status()

    # def toggleswitch_1_x_change(self, **event_args):
    #     # Update the label text based on the toggle switch state
    #     self.label_9.text = "x_change fired : " + ("yes" if self.toggleswitch_1.checked else "No")
        
    #     # Get the status from the toggle switch state
    #     status = 'yes' if self.toggleswitch_1.checked else 'no'
        
    #     # Update the switch and call the update_loan_status method
    #     if status == 'yes':
    #         self.switch_1.value = True
    #         self.update_loan_status('home_loan', 'yes')
    #     elif status == 'no':
    #         self.switch_1.value = False
    #         self.update_loan_status('home_loan', 'no')

    
    def toggleswitch_2_x_change(self, **event_args):
        self.toggleswitch_2_interacted = True
        # Update the label text based on the toggle switch state
        self.label_2.text = "Yes" if self.toggleswitch_2.checked else "No"
        
        # Get the status from the toggle switch state
        status = 'yes' if self.toggleswitch_2.checked else 'no'
        # Update the switch and call the update_loan_status method
        if status == 'yes':
            self.toggleswitch_2.value = True
            self.update_loan_status('other_loan', 'yes')
        elif status == 'no':
            self.toggleswitch_2.value = False
            self.update_loan_status('other_loan', 'no')

    def toggleswitch_3_x_change(self, **event_args):
        self.toggleswitch_3_interacted = True
        # Update the label text based on the toggle switch state
        self.label_7.text = "Yes" if self.toggleswitch_3.checked else "No"
        
        # Get the status from the toggle switch state
        status = 'yes' if self.toggleswitch_3.checked else 'no'
        
        # Update the switch and call the update_loan_status method
        if status == 'yes':
            self.toggleswitch_3.value = True
            self.update_loan_status('credit_card_loans', 'yes')
        elif status == 'no':
            self.toggleswitch_3.value = False
            self.update_loan_status('credit_card_loans', 'no')
    def toggleswitch_4_x_change(self, **event_args):
        self.toggleswitch_4_interacted = True
        # Update the label text based on the toggle switch state
        self.label_8.text = "Yes" if self.toggleswitch_4.checked else "No"
        
        # Get the status from the toggle switch state
        status = 'yes' if self.toggleswitch_4.checked else 'no'
        
        # Update the switch and call the update_loan_status method
        if status == 'yes':
            self.toggleswitch_4.value = True
            self.update_loan_status('vehicle_loan', 'yes')
        elif status == 'no':
            self.toggleswitch_4.value = False
            self.update_loan_status('vehicle_loan', 'no')
    
    def next_click(self, **event_args):
        """This method is called when the button is clicked"""
        # if not self.toggleswitch_1.checked or not self.toggleswitch_2.checked or not self.toggleswitch_3.checked or not self.toggleswitch_4.checked or not self.toggleswitch_1.unchecked or not self.toggleswitch_2.unchecked or not self.toggleswitch_3.unchecked or not self.toggleswitch_4.unchecked:
        #     alert("Please select  loan status before proceeding.")
        if not (self.toggleswitch_1_interacted and self.toggleswitch_2_interacted and self.toggleswitch_3_interacted and self.toggleswitch_4_interacted):
            alert("Please select all loan status toggle switches Yes or No before proceeding.")
        else:
            anvil.server.call('add_borrower_step4', self.home_loan_status, 
                              self.other_loan_status, self.user_id,
                              self.credit_card_loan_status, self.vehicle_loan_status)
            open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_5_bank_1', user_id=self.user_id)

    def button_1_click(self, **event_args):
        open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital', user_id=self.user_id)

    def home_borrower_registration_form_click(self, **event_args):
        open_form('bank_users.main_form.investNow_applyForLoan')

       
    def toggleswitch_1_x_change(self, **event_args):
        self.toggleswitch_1_interacted = True
      # Update the label text based on the toggle switch state
        self.label_1.text = "Yes" if self.toggleswitch_1.checked else "No"
        
        # Get the status from the toggle switch state
        status = 'yes' if self.toggleswitch_1.checked else 'no'
        
        # Update the switch and call the update_loan_status method
        if status == 'yes':
            self.toggleswitch_1.value = True
            self.update_loan_status('home_loan', 'yes')
        elif status == 'no':
            self.toggleswitch_1.value = False
            self.update_loan_status('home_loan', 'no')

      


      
