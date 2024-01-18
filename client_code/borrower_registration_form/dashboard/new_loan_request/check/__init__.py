from datetime import datetime, timedelta
import anvil.server
import anvil.tables as tables
from anvil import DataGrid, alert, open_form
from ._anvil_designer import checkTemplate
from .. import main_form_module as main_form_module

class check(checkTemplate):
    def __init__(self, product_group, product_cat, loan_amount, tenure_months, user_id, interest_rate, processing_fee, membership_type, product_id, total_repayment_amount, credit_limt, entered_values=None, **properties):
        self.product_group = product_group
        self.product_cat = product_cat
        self.loan_amount = int(loan_amount)
        self.tenure_months = int(tenure_months)
        self.user_id = user_id
        self.interest_rate = float(interest_rate)
        self.processing_fee = float(processing_fee)
        self.membership_type = membership_type
        self.product_id = product_id
        self.total_repayment_amount = float(total_repayment_amount)
        self.credit_limt = credit_limt

        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Load previously entered values when form is initialized
        self.load_entered_values(entered_values)

        # Create an empty list to store payment details
        payment_details = []

        # Monthly interest rate
        monthly_interest_rate = (self.interest_rate / 100) / 12

        # Extra payment amount (initialized with 0 for all months)
        extra_payment = 0

        # Calculate EMI (monthly installment)
        emi = (self.loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** self.tenure_months)) / (
                ((1 + monthly_interest_rate) ** self.tenure_months) - 1)

        # Initialize the first beginning balance with the initial loan amount
        beginning_balance = self.loan_amount
        payment_date_placeholder = "Awaiting update"

        # Calculate payment details for each month up to the tenure
        for month in range(1, self.tenure_months + 1):
            # Calculate interest amount for the month
            interest_amount = beginning_balance * monthly_interest_rate

            # Calculate principal amount for the month
            principal_amount = emi - interest_amount

            # Update ending balance for the current iteration
            ending_balance = beginning_balance - principal_amount

           

            # Add payment details to the list
            payment_details.append({
                'PaymentNumber': month,
                'PaymentDate': payment_date_placeholder,
                'ScheduledPayment': f"₹ {emi:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'ExtraPayment': f"₹ {extra_payment:.2f}",  # Extra payment column
                'TotalPayment': f"₹ {emi + extra_payment:.2f}",  # Include extra payment in the total payment
                'EndingBalance': f"₹ {ending_balance:.2f}"
            })

            # Update beginning balance for the next iteration
            beginning_balance = ending_balance

        # Set the Data Grid's items property to the list of payment details
        self.repeating_panel_1.items = payment_details

    def load_entered_values(self, entered_values):
        if entered_values:
            # Load previously entered values into the form fields
            self.entered_loan_amount = entered_values.get('loan_amount', None)
            self.entered_tenure = entered_values.get('tenure', None)
            self.entered_payment_type = entered_values.get('payment_type', None)

    def submit_click(self, **event_args):
        # Call the server function to add loan details
        result = anvil.server.call('add_loan_details',
                                   self.loan_amount,
                                   self.tenure_months,
                                   self.user_id,
                                   self.interest_rate,
                                   self.total_repayment_amount,
                                   self.product_id,
                                   self.membership_type,
                                   self.credit_limt)

        # Log the result for debugging
        print(result)

        # Show alert and navigate to the borrower dashboard
        alert("Request Submitted")
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        open_form('borrower_registration_form.dashboard.new_loan_request.loan_type',
                  self.product_group,
                  self.product_cat,
                  entered_values={
                      'loan_amount': self.entered_loan_amount,
                      'tenure': self.entered_tenure,
                      'payment_type': self.entered_payment_type
                  })

    def button_1_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')
