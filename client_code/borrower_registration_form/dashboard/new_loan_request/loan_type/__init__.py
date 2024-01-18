from anvil import open_form, alert
from .. import main_form_module as main_form_module
from ... import app_tables
from ._anvil_designer import loan_typeTemplate

class loan_type(loan_typeTemplate):
    def __init__(self, product_group, product_cat, max_amount_lb, entered_values=None, **properties):
        self.user_id = main_form_module.userId
        self.proctct_g = product_group
        self.prodct_cate = product_cat
        self.credit_limt = max_amount_lb
        self.init_components(**properties)

        # Initialize instance variables to store entered values
        self.entered_loan_amount = None
        self.entered_tenure = None
        self.entered_payment_type = None

        # Load previously entered values when form is initialized
        self.load_entered_values(entered_values)

        # user_request = app_tables.fin_product_details.get(product_categories=self.prodct_cate)
        user_request = app_tables.fin_product_details.get(product_categories=product_cat)
        if user_request:
            self.roi = user_request['roi']
            self.processing_fee = user_request['processing_fee']
            self.membership_type = user_request['membership_type']
            self.product_id = user_request['product_id']
            self.emi_payment_options = user_request['emi_payment']

            # Show/hide and adjust properties of radio buttons based on emi_payment options
            self.set_radio_button_visibility()

    def load_entered_values(self, entered_values):
        if entered_values:
            # Load previously entered values into the form fields
            self.entered_loan_amount = entered_values.get('loan_amount', None)
            self.entered_tenure = entered_values.get('tenure', None)
            self.entered_payment_type = entered_values.get('payment_type', None)

            if self.entered_loan_amount is not None:
                self.loan_amount_tb.text = str(self.entered_loan_amount)
            if self.entered_tenure is not None:
                self.text_box_1.text = str(self.entered_tenure)
            if self.entered_payment_type is not None:
                # Set the selected radio button based on the stored value
                self.set_selected_payment_type(self.entered_payment_type)

    def set_selected_payment_type(self, payment_type):
        # Set the selected payment type based on the stored value
        if payment_type == "One Time":
            self.radio_button_1.selected = True
        elif payment_type == "Monthly":
            self.radio_button_2.selected = True
        elif payment_type == "Three Month":
            self.radio_button_3.selected = True
        elif payment_type == "Six Month":
            self.radio_button_4.selected = True

    def set_radio_button_visibility(self):
        visible_options = [emi_option for emi_option in ["One Time", "Monthly", "Three Month", "Six Month"] if emi_option in self.emi_payment_options]

        for i, emi_option in enumerate(visible_options):
            radio_button = getattr(self, f'radio_button_{i + 1}')
            radio_button.visible = True
            radio_button.text = emi_option
            radio_button.x = 20 + i * 150  # Adjust the value (20 and 150) according to your layout preference

    def button_1_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        open_form('borrower_registration_form.dashboard.new_loan_request')

    def button_3_click(self, **event_args):
        loan_amount = self.loan_amount_tb.text
        tenure = self.text_box_1.text
        payment_type = self.get_selected_payment_type()

        # Save entered values for persistence
        self.entered_loan_amount = loan_amount
        self.entered_tenure = tenure
        self.entered_payment_type = payment_type
        self.membership_type = self.membership_type

        # Validate loan_amount and tenure (similar to your existing validation code)
        if not any([self.label_22.text, self.label_23.text]):
            # If validations pass, open the 'check' form and pass the values
            open_form('borrower_registration_form.dashboard.new_loan_request.check',
                      self.proctct_g, self.prodct_cate, str(loan_amount), tenure,
                      self.user_id, self.roi, self.processing_fee,
                      self.membership_type, self.product_id,
                      self.Total_Repayment_Amount,self.credit_limt,
                      entered_values={
                          'loan_amount': self.entered_loan_amount,
                          'tenure': self.entered_tenure,
                          'payment_type': self.entered_payment_type
                      })

    def fetch_product_data(self):
        return app_tables.fin_product_details.search(
            product_group=self.proctct_g,
            product_categories=self.prodct_cate
        )



    def get_min_max_amount(self):
        product_data = self.fetch_product_data()
        if product_data:
            min_amount = product_data[0]['min_amount']
            max_amount = product_data[0]['max_amount']
            return min_amount, max_amount
        return 0, 0

    def get_min_max_tenure(self):
        product_data = self.fetch_product_data()
        if product_data:
            min_tenure = product_data[0]['min_tenure']
            max_tenure = product_data[0]['max_tenure']
            return min_tenure, max_tenure
        return 0, 0

    def display_label_text(self, label, column_name):
        product_data = self.fetch_product_data()
        if product_data:
            label_text = [str(data[column_name]) for data in product_data]
            label.text = label_text[0] if label_text else None

    def label_11_show(self, **event_args):
        self.display_label_text(self.label_11, 'max_amount')

    def label_5_show(self, **event_args):
        self.display_label_text(self.label_5, 'min_amount')

    def label_13_show(self, **event_args):
        self.display_label_text(self.label_13, 'min_tenure')

    def label_15_show(self, **event_args):
        self.display_label_text(self.label_15, 'max_tenure')

    def label_21_show(self, **event_args):
        self.display_label_text(self.label_21, 'processing_fee')

    def label_7_show(self, **event_args):
        self.display_label_text(self.label_7, 'roi')

    def label_9_show(self, **event_args):
        self.display_label_text(self.label_9, 'foreclose_type')

    def label_18_show(self, **event_args):
        self.display_label_text(self.label_18, 'membership_type')

    def button_4_click(self, **event_args):
        loan_amount = self.loan_amount_tb.text
        tenure = self.text_box_1.text
        one_time = self.radio_button_1.selected
        monthly_emi = self.radio_button_2.selected
        three_month = self.radio_button_3.selected
        six_month = self.radio_button_4.selected

        if not loan_amount:
            self.label_22.text = "Please fill the loan amount"
            self.label_22.foreground = '#FF0000'
        elif not loan_amount.isdigit():
            self.label_22.text = "Please enter only numeric values (0-9) for loan amount"
            self.label_22.foreground = '#FF0000'
        else:
            min_amount, max_amount = self.get_min_max_amount()
            loan_amount = int(loan_amount)

            if min_amount <= loan_amount <= max_amount:
                self.label_22.text = ""
            else:
                self.label_22.text = f"Loan amount should be between {min_amount} and {max_amount}"
                self.label_22.foreground = '#FF0000'

        # Validate tenure
        if not tenure:
            self.label_23.text = "Please select tenure"
            self.label_23.foreground = '#FF0000'
        elif not tenure.isdigit():
            self.label_23.text = "Please enter only numeric values (0-9) for tenure"
            self.label_23.foreground = '#FF0000'
        else:
            min_tenure, max_tenure = self.get_min_max_tenure()
            tenure = int(tenure)

            if min_tenure <= tenure <= max_tenure:
                self.label_23.text = ""
            else:
                self.label_23.text = f"Tenure should be between {min_tenure} and {max_tenure}"
                self.label_23.foreground = '#FF0000'

        # Validate radio_button_1 and radio_button_2
        if not (one_time or monthly_emi or three_month or six_month):
            self.label_24.text = "Please select the EMI Payment Type"
            self.label_24.foreground = '#FF0000'
        else:
            self.label_24.text = ""

        # Proceed to the next form only if all validations pass
        if not any([self.label_22.text, self.label_23.text, self.label_24.text]):
            self.grid_panel_2.visible = True
            self.button_2.visible = True
            self.button_3.visible = True
            self.button_5.visible = True
            self.button_4.visible = False

            self.label_28.text = f"₹ {loan_amount}"
            p = float(loan_amount)
            t = int(tenure)
            r = float(int(self.roi)/100)
            interest_amount = p * r
            self.label_30.text = f"₹ {int(interest_amount)}"
            processing_fee_amount = float((self.processing_fee/100) * p)
            self.label_32.text = f"₹ {int(processing_fee_amount)}"
            self.Total_Repayment_Amount = float(p + interest_amount + processing_fee_amount)
            Monthly_EMI = int(self.Total_Repayment_Amount / float(t))
            self.label_36.text = f"₹ {int(Monthly_EMI)}"
            self.label_34.text = f"₹ {int(self.Total_Repayment_Amount)}"

            # Disable editing after clicking button_4
            self.loan_amount_tb.enabled = False
            self.text_box_1.enabled = False
            self.radio_button_1.enabled = False
            self.radio_button_2.enabled = False
            self.radio_button_3.enabled = False
            self.radio_button_4.enabled = False

    def button_5_click(self, **event_args):
        self.loan_amount_tb.enabled = True
        self.text_box_1.enabled = True
        self.radio_button_1.enabled = True
        self.radio_button_2.enabled = True
        self.radio_button_3.enabled = True
        self.radio_button_4.enabled = True
        self.grid_panel_2.visible = False
        self.button_2.visible = False
        self.button_3.visible = False
        self.button_5.visible = False
        self.button_4.visible = True

    def get_selected_payment_type(self):
        # Return the selected payment type based on the radio buttons
        if self.radio_button_1.selected:
            return "One Time"
        elif self.radio_button_2.selected:
            return "Monthly"
        elif self.radio_button_3.selected:
            return "Three Month"
        elif self.radio_button_4.selected:
            return "Six Month"
        else:
            return None

# Instantiate the form
loan_type_1 = loan_type('product_group_value', 'product_cat_value','self.credit_limt')

# Open the form
open_form(loan_type_1)

