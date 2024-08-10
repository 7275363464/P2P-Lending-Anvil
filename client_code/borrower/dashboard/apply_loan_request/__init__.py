from ._anvil_designer import apply_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from .. import main_form_module

class apply_loan_request(apply_loan_requestTemplate):
    def __init__(self, **properties):
        self.user_id = main_form_module.userId
        self.product_description = None
        self.init_components(**properties)

        options = app_tables.fin_product_details.search()
        option_strings = [option['product_group'] for option in options if option['product_group'].strip()]
        unique_groups = set(option_strings)  # Remove duplicates using set
        self.name.items = list(unique_groups)
        self.name.selected_value = None 
        self.drop_down_2.items = ['']  # Add your placeholder text here
        self.drop_down_2.selected_value = None
        self.drop_down_1.items = ['']
        self.drop_down_1.selected_value = None
        self.drop_down_3.items = ['']
        self.drop_down_3.selected_value = None
        # self.drop_down_3_change()

    def name_change(self, **event_args):
        self.selected_value = self.name.selected_value

        if self.selected_value:
            self.label_1.visible = True
            self.label_2.visible = True
            self.name.visible = True
            self.drop_down_2.visible = True
            self.label_4.visible = True
            # Fetch product categories based on the selected loan type
            product_categories = app_tables.fin_product_details.search(
                product_group=self.name.selected_value
            )
            # Exclude duplicate categories
            unique_categories = set(category['product_categories'] for category in product_categories if category['product_categories'].strip())
            if unique_categories:
                # Display unique product categories in drop_down_2
                self.drop_down_2.items = list(unique_categories)
                self.drop_down_2.selected_value = None

    def drop_down_2_change(self, **event_args):
        self.selected_value = self.drop_down_2.selected_value
        if self.selected_value:
            self.label_1.visible = True
            self.label_2.visible = True
            self.name.visible = True
            self.drop_down_2.visible = True
            self.label_4.visible = True
            self.label_6.visible = True
            self.label_7.visible = True
            self.drop_down_1.visible = True

            # Fetch product names based on the selected category
            product_names = app_tables.fin_product_details.search(product_categories=self.selected_value)
            if product_names:
                # Extract product names from the list of rows
                product_name_list = [product['product_name'] for product in product_names if product['product_name'].strip()]
                self.drop_down_1.items = product_name_list
                self.drop_down_1.selected_value = None

    def drop_down_1_change(self, **event_args):
        selected_product_name = self.drop_down_1.selected_value
        # self.link_2.visible = True
        if selected_product_name:
            product_details = app_tables.fin_product_details.get(product_name=selected_product_name)

            if product_details:
                self.label_8.visible = True
                self.product_description_label.visible = True
                self.product_description_label.text = product_details['product_description']
                self.drop_down_3_change()
                self.link_2_click()
                self.link_1.visible = True
            else:
                self.label_8.visible = True
                self.product_description_label.visible = True
                self.product_description_label.text = "Product description not available"
        else:
            self.label_8.visible = False
            self.product_description_label.visible = True
            self.product_description_label.text = ""

    def link_2_click(self, **event_args):      
      # self.drop_down_3_change()
      name = self.name.selected_value
      category = self.drop_down_2.selected_value
      product_name = self.drop_down_1.selected_value

      if not name:
          self.label_3.text = "Please select a product group"
          self.label_3.foreground = '#FF0000'
      else:
          self.label_3.text = ""

      if not category:
          self.label_4.text = "Please select a category"
          self.label_4.foreground = '#FF0000'
      else:
          self.label_4.text = ""

      if not product_name:
          self.label_7.text = "Please select a product name"
          self.label_7.foreground = '#FF0000'
      else:
          self.label_7.text = ""

      if name and category and product_name:
          if any(row['product_name'] == product_name for row in app_tables.fin_loan_details.search(borrower_customer_id=self.user_id)):
              self.name.selected_value = None
              self.drop_down_1.selected_value = None
              self.drop_down_2.selected_value = None
              alert(f'Product "{product_name}" already exists. Please choose a different Product name.')
          else:
              # Fetch product details based on the selected product name
              product_details = app_tables.fin_product_details.get(product_name=product_name)
              if product_details:
                  # Set product_description as a class attribute
                  self.product_description = product_details['product_description']
                  # self.interest_rate = product_details['interest_rate']
                  # self.processing_fee = product_details['processing_fee']
                  # self.tenure_months = product_details['tenure_months']
                  # self.loan_amount = product_details['loan_amount']
                  # self.credit_limit = product_details['credit_limit']
                  # self.calculate_and_display_payment_details()
                  self.link_2.visible = False
                  self.label_2_copy.visible = True
                  self.loan_amount_tb.visible = True
                  self.label_22.visible = True
                  self.label_4_copy.visible = True
                  self.label_7_copy.visible = True
                  self.label_20.visible = True
                  self.label_21.visible = True
                  self.label_23.visible = True
                  self.label_3_copy.visible = True
                  self.text_box_1.visible = True
                  self.label_39.visible = True
                  self.drop_down_3.visible = True
                  
                  # self.link_1.visible = True
                  self.product_name = self.drop_down_1.selected_value
                  user_request = app_tables.fin_product_details.get(product_name=self.product_name)
                  if user_request:
                    self.label_7_copy.text = user_request['roi']
                    self.label_21.text = user_request['processing_fee']
              else:
                  self.label_8.visible = True
                  self.product_description_label.text = "Product description not available"

    def link_1_click(self, **event_args):
        self.label_29.text = f"Total Interest Amount({self.label_7_copy.text}%)"
        self.label_31.text = f"Processing fee Amount({self.label_21.text}%)"
        loan_amount = self.loan_amount_tb.text
        tenure = self.text_box_1.text
        emi_type = self.drop_down_3.selected_value
        # one_time = self.button_1_1.background == '#0a2346'
        # monthly_emi = self.button_2_1.background == '#0a2346'
        # three_months = self.button_3_1.background == '#0a2346'
        # six_months = self.button_4_1.background == '#0a2346'

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

        if not emi_type:
            self.label_24.text = "Please select the EMI Payment Type"
            self.label_24.foreground = '#FF0000'
        else:
            self.label_24.text = ""

            if not any([self.label_22.text, self.label_23.text, self.label_24.text]):
                self.column_panel_3.visible = True
                self.link_1.visible = False
                self.label_28.text = f"₹ {loan_amount}"
                p = loan_amount
                t = tenure
                monthly_interest_rate = float(self.label_7_copy.text) / 100 / 12

              
                # print("ROI:", self.roi)
                # monthly_interest_rate = float(int(self.roi) / 100) / 12
                # print("Monthly Interest Rate:", monthly_interest_rate)
              
                emi_denominator = ((1 + monthly_interest_rate) ** t) - 1
                print('denominatio' , emi_denominator)
                emi_numerator = p * monthly_interest_rate * ((1 + monthly_interest_rate) ** t)
                print('numerator' , emi_numerator)
                Monthly_EMI = emi_numerator / emi_denominator
                print('monthly emi' , Monthly_EMI)
              
                self.label_36.text = f"₹ {Monthly_EMI:.2f}"
                interest_amount = Monthly_EMI * t - p
                self.label_30.text = f"₹ {interest_amount:.2f}"
                processing_fee_amount = (float(self.label_21.text) / 100) * p
                self.label_32.text = f"₹ {processing_fee_amount:.2f}"
                self.Total_Repayment_Amount = round(p + interest_amount + processing_fee_amount ,2)
                self.label_34.text = f"₹ {self.Total_Repayment_Amount:.2f}"
                self.emi = Monthly_EMI
                self.link_1.visible = False
                self.column_panel_3.visible = True
                self.submit.visible = True

    def link_3_click(self, **event_args):
        # Toggle the visibility of the column_panel_1
        if self.column_panel_1.visible:
            self.column_panel_1.visible = False
            self.link_3.text = "View Payment details"
        else:
            self.column_panel_1.visible = True
            self.link_3.text = "Hide Details"
            self.calculate_and_display_payment_details()
      

    def drop_down_3_change(self, **event_args):
        # This method is called when an item is selected in drop_down_3
        self.selected_value = self.drop_down_3.selected_value
        product_group = self.name.selected_value
        product_category = self.drop_down_2.selected_value
        product_name = self.drop_down_1.selected_value
        # self.link_1.visible = True
    
        if product_group and product_category and product_name:
            # Fetch the data from fin_product_details based on the product_group, product_category, and product_name
            product_details = app_tables.fin_product_details.search(
                product_group=product_group,
                product_categories=product_category,
                product_name=product_name
            )
            product_details = list(product_details)
            if product_details:
                product_detail = product_details[0]
                emi_payment_options = product_detail['emi_payment']
                emi_payment_options = emi_payment_options.split(", ") if emi_payment_options else []
                self.drop_down_3.items = emi_payment_options
                # self.link_1.visible = True
                self.column_panel_3.visible = False
                self.submit.visible = False


  
    def calculate_and_display_payment_details(self):
        self.entered_payment_type = self.drop_down_3.selected_value
        self.total_interest = self.label_30.text
        if self.entered_payment_type == "One Time":
            self.display_one_time_payment_details()
        elif self.entered_payment_type == "Monthly":
            self.display_monthly_payment_details()
        elif self.entered_payment_type == "Three Months":
            self.display_three_month_payment_details(total_interest_amount=self.total_interest)
        elif self.entered_payment_type == "Six Months":
            self.display_six_month_payment_details(total_interest_amount=self.total_interest)

    def display_one_time_payment_details(self):
        # Remove currency symbols and convert text to float
        total_repayment_amount = float(self.label_34.text.replace('₹ ', '').replace(',', ''))
        total_interest = float(self.label_30.text.replace('₹ ', '').replace(',', ''))
        processing_fee_amount = float(self.label_32.text.replace('₹ ', '').replace(',', ''))
        loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', ''))
    
        payment_details = [{
            'PaymentNumber': 'EMI 1',
            'Principal': f"₹ {loan_amount:,.2f}",
            'Interest': f"₹ {total_interest:,.2f}",
            'ProcessingFee': f"₹ {processing_fee_amount:,.2f}",
            'BeginningBalance': f"₹ {total_repayment_amount:,.2f}",
            'TotalPayment': f"₹ {total_repayment_amount:,.2f}",
            'EndingBalance': '₹ 0.00',
            'LoanAmountBeginningBalance': f"₹ {loan_amount:,.2f}",
            'LoanAmountEndingBalance': '₹ 0.00'
        }]
        
        self.repeating_panel_1.items = payment_details

    def display_monthly_payment_details(self):
        # Convert the necessary text values to float or int
        user_request = app_tables.fin_product_details.get(product_name=self.product_name)
        total_repayment_amount = float(self.label_34.text.replace('₹ ', '').replace(',', '').strip())
        # interest_rate = float(self.label_7_copy.text.replace('%', '').strip())
        interest_rate = user_request['roi']
        tenure_months = int(self.text_box_1.text.strip())
        loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
    
        # Calculate monthly interest rate
        monthly_interest_rate = interest_rate / 100 / 12
    
        # Calculate EMI
        emi_denominator = ((1 + monthly_interest_rate) ** tenure_months) - 1
        emi_numerator = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months)
        emi = emi_numerator / emi_denominator
    
        # Generate the payment schedule
        payment_details = self.calculate_payment_schedule(total_repayment_amount, emi, monthly_interest_rate)
    
        # Set the items for the repeating panel
        self.repeating_panel_1.items = payment_details

    def calculate_payment_schedule(self, total_repayment_amount, emi, monthly_interest_rate):
        user_request = app_tables.fin_product_details.get(product_name=self.product_name)
        self.processing_fee = float(user_request['processing_fee'])
        self.tenure_months = int(self.text_box_1.text)
        self.loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
    
        payment_schedule = []
        processing_fee_per_month = (self.processing_fee / 100) * self.loan_amount / self.tenure_months
        beginning_balance = total_repayment_amount
        loan_amount_beginning_balance = self.loan_amount
    
        for month in range(1, self.tenure_months + 1):
            interest_amount = loan_amount_beginning_balance * monthly_interest_rate
            principal_amount = emi - interest_amount
            total_payment = emi + processing_fee_per_month
            loan_amount_ending_balance = loan_amount_beginning_balance - principal_amount
            payment_schedule.append({
                'PaymentNumber': f"EMI {month}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
                'LoanAmountBeginningBalance': f"₹ {loan_amount_beginning_balance:.2f}",
                'LoanAmountEndingBalance': f"₹ {loan_amount_ending_balance:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'TotalPayment': f"₹ {total_payment:.2f}",
                'EndingBalance': f"₹ {max(0, beginning_balance - total_payment):.2f}"
            })
            beginning_balance -= total_payment
            loan_amount_beginning_balance = loan_amount_ending_balance
    
        return payment_schedule

    def display_three_month_payment_details(self, total_interest_amount):
        # Convert the necessary text values to float or int
        user_request = app_tables.fin_product_details.get(product_name=self.product_name)
        interest_rate = user_request['roi']
        # interest_rate = float(self.label_7_copy.text.replace('%', '').strip())
        tenure_months = int(str(self.text_box_1.text).strip())  # Ensure this is treated as a string first, then convert to int
        loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
        # processing_fee = float(self.label_21.text.replace('%', '').strip())
        processing_fee = user_request['processing_fee']
        
        # Calculate monthly interest rate
        monthly_interest_rate = interest_rate / 100 / 12
    
        # Calculate EMI
        emi_denominator = ((1 + monthly_interest_rate) ** tenure_months) - 1
        emi_numerator = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months)
        emi = emi_numerator / emi_denominator
    
        # Calculate processing fee per month
        processing_fee_per_month = (processing_fee / 100) * loan_amount / tenure_months
    
        # Generate the payment schedule
        payment_schedule = self.calculate_three_month_payment_schedule(emi, monthly_interest_rate, processing_fee_per_month, total_interest_amount)
        
        # Set the items for the repeating panel
        self.repeating_panel_1.items = payment_schedule

    def calculate_three_month_payment_schedule(self, emi, monthly_interest_rate, processing_fee_per_month, total_interest_amount):
        # Convert the necessary text values to float
        loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
        total_repayment_amount = float(self.label_34.text.replace('₹ ', '').replace(',', '').strip())
        tenure_months = int(str(self.text_box_1.text).strip())
        # tenure_months = int(self.tenure_months)  # Ensure tenure_months is an integer
    
        payment_schedule = []
        beginning_balance = total_repayment_amount
        loan_amount_beginning_balance = loan_amount
    
        for month in range(1, tenure_months + 1, 3):
            # Calculate interest for 3 months
            interest_for_3_months = self.calculate_interest_for_months(emi, loan_amount_beginning_balance, monthly_interest_rate, month, month + 2)
            
            total_processing_fee_for_3_months = processing_fee_per_month * 3
            total_payment = emi * 3 + total_processing_fee_for_3_months
            
            payment_schedule.append({
                'PaymentNumber': f"EMI {month}-{month + 2}",
                'Principal': f"₹ {emi * 3 - interest_for_3_months:.2f}",
                'Interest': f"₹ {interest_for_3_months:.2f}",
                'ProcessingFee': f"₹ {total_processing_fee_for_3_months:.2f}",
                'LoanAmountBeginningBalance': f"₹ {loan_amount_beginning_balance:.2f}",
                'LoanAmountEndingBalance': f"₹ {loan_amount_beginning_balance - (emi * 3 - interest_for_3_months):.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'TotalPayment': f"₹ {total_payment:.2f}",
                'EndingBalance': f"₹ {max(0, beginning_balance - total_payment):.2f}"
            })
    
            beginning_balance -= total_payment
            loan_amount_beginning_balance -= (emi * 3 - interest_for_3_months)
        
        return payment_schedule

    def display_six_month_payment_details(self, total_interest_amount):
        # Convert the necessary text values to float or int
        user_request = app_tables.fin_product_details.get(product_name=self.product_name)
        interest_rate = user_request['roi']
        processing_fee = user_request['processing_fee']
        # interest_rate = float(self.label_7_copy.text.replace('%', '').strip())
        tenure_months = int(self.text_box_1.text.strip())
        loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
        # processing_fee = float(self.label_21.text.replace('%', '').strip())
    
        # Calculate monthly interest rate
        monthly_interest_rate = interest_rate / 100 / 12
    
        # Calculate EMI
        emi_denominator = ((1 + monthly_interest_rate) ** tenure_months) - 1
        emi_numerator = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months)
        emi = emi_numerator / emi_denominator
    
        # Calculate processing fee per month
        processing_fee_per_month = (processing_fee / 100) * loan_amount / tenure_months
    
        # Generate the payment schedule
        payment_schedule = self.calculate_six_month_payment_schedule(emi, monthly_interest_rate, processing_fee_per_month, total_interest_amount)
        
        # Set the items for the repeating panel
        self.repeating_panel_1.items = payment_schedule

    def calculate_six_month_payment_schedule(self, emi, monthly_interest_rate, processing_fee_per_month, total_interest_amount):
        # Convert loan_amount and total_repayment_amount to floats after cleaning the text
        self.loan_amount = float(self.label_28.text.replace('₹ ', '').replace(',', '').strip())
        self.total_repayment_amount = float(self.label_34.text.replace('₹ ', '').replace(',', '').strip())
        self.tenure_months = int(str(self.text_box_1.text).strip())
    
        payment_schedule = []
        beginning_balance = self.total_repayment_amount
        loan_amount_beginning_balance = self.loan_amount
    
        for month in range(1, self.tenure_months + 1, 6):
            interest_for_6_months = self.calculate_interest_for_months(emi, loan_amount_beginning_balance, monthly_interest_rate, month, month + 5)
            total_processing_fee_for_6_months = processing_fee_per_month * 6
            total_payment = emi * 6 + total_processing_fee_for_6_months
    
            principal_payment = emi * 6 - interest_for_6_months
            loan_amount_ending_balance = loan_amount_beginning_balance - principal_payment
            ending_balance = max(0, beginning_balance - total_payment)
    
            payment_schedule.append({
                'PaymentNumber': f"EMI {month}-{month+5}",
                'Principal': f"₹ {principal_payment:.2f}",
                'Interest': f"₹ {interest_for_6_months:.2f}",
                'ProcessingFee': f"₹ {total_processing_fee_for_6_months:.2f}",
                'LoanAmountBeginningBalance': f"₹ {loan_amount_beginning_balance:.2f}",
                'LoanAmountEndingBalance': f"₹ {loan_amount_ending_balance:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'TotalPayment': f"₹ {total_payment:.2f}",
                'EndingBalance': f"₹ {ending_balance:.2f}"
            })
    
            beginning_balance = ending_balance
            loan_amount_beginning_balance = loan_amount_ending_balance
    
        return payment_schedule

    def calculate_interest_for_months(self, emi, loan_amount_beginning_balance, monthly_interest_rate, start_month, end_month):
        # Check if loan_amount_beginning_balance is a string and clean it if necessary
        if isinstance(loan_amount_beginning_balance, str):
            loan_amount_beginning_balance = float(loan_amount_beginning_balance.replace('₹ ', '').replace(',', '').strip())
    
        total_interest = 0
        for month in range(start_month, end_month + 1):
            interest_amount = loan_amount_beginning_balance * monthly_interest_rate
            loan_amount_beginning_balance -= (emi - interest_amount)
            total_interest += interest_amount
    
        return total_interest

  
    def submit_click(self, **event_args):
        self.interest_rate = float(str(self.label_7_copy.text).replace('%', '').strip())
        self.tenure_months = int(str(self.text_box_1.text).strip())
        self.loan_amount = float(str(self.label_28.text).replace('₹ ', '').replace(',', '').strip())
        self.total_repayment_amount = float(str(self.label_34.text).replace('₹ ', '').replace(',', '').strip())
        # processing_fee = float(self.label_21.text.replace('%', '').strip())
        self.product_group = self.name.selected_value
        self.product_category = self.drop_down_2.selected_value
        self.product_name = self.drop_down_1.selected_value
        user_request = app_tables.fin_product_details.get(product_name=self.product_name)
        # self.product_details = app_tables.fin_product_details.search(
        #         product_group=self.product_group,
        #         product_categories=self.product_category,
        #         product_name=self.product_name
        # )
        self.product_id = user_request['product_id']
        self.membership_type = user_request['membership_type']
        self.credit_limt = user_request['max_amount']
        self.entered_payment_type = self.drop_down_3.selected_value
        self.processing_fee_amount = float(str(self.label_32.text).replace('₹ ', '').replace(',', ''))
        self.total_interest = float(str(self.label_30.text).replace('₹ ', '').replace(',', ''))
        self.product_discription = self.product_description_label.text
        result = anvil.server.call('add_loan_details',
                                  self.loan_amount,
                                  self.tenure_months,
                                  self.user_id,
                                  self.interest_rate,
                                  self.total_repayment_amount,
                                  self.product_id,
                                  self.membership_type,
                                  self.credit_limt,
                                  self.product_name,
                                  self.entered_payment_type,
                                  self.processing_fee_amount,
                                  self.total_interest,
                                  self.product_discription,
                                  self.emi)
    
        print(result)
        alert("Request Submitted")
        open_form('borrower.dashboard')


    def fetch_product_data(self):
        return app_tables.fin_product_details.search(
            product_group=self.name.selected_value,
            product_categories=self.drop_down_2.selected_value,
            product_name = self.drop_down_1.selected_value
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

    def loan_amount_tb_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        loan_amount = self.loan_amount_tb.text
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

    def text_box_1_change(self, **event_args):
        tenure = self.text_box_1.text
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
