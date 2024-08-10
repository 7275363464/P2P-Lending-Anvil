# from ._anvil_designer import lendersTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class lenders(lendersTemplate):
#     def __init__(self, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)

#         # Any code you write here will run before the form opens.
#         self.data = app_tables.fin_user_profile.search()

#         self.result = []
#         for user_profile in self.data:
#             if user_profile['usertype'] == 'lender':
#                 # Retrieve credit limit from fin_lender table based on customer ID
#                 # lender_record = app_tables.fin_lender.get(customer_id=user_profile['customer_id'])
#                 # if lender_record is not None:
#                 #     credit_limit = lender_record['credit_limit']
#                 # else:
#                 #     credit_limit = None
              
#                 # Retrieve guarantor details from fin_guarantor table based on customer ID
#                 guarantor_record = app_tables.fin_guarantor_details.get(customer_id=user_profile['customer_id'])
#                 if guarantor_record is not None:
#                     guarantor_name = guarantor_record['guarantor_name']
#                     guarantor_ph_no = guarantor_record['guarantor_mobile_no']
#                     guarantor = guarantor_record['another_person']
#                 else:
#                     guarantor_name = None
#                     guarantor_ph_no = None
#                     guarantor = None
#                 loan_details = app_tables.fin_lender.get(customer_id=user_profile['customer_id'])
#                 if loan_details is not None:
#                   membership_type = loan_details['membership']
#                   member_since  = loan_details['member_since']
#                 else:
#                   membership_type = None
#                   member_since = None
              
#                 # Count loan details with specific loan_updated_status
#                 loan_details_count = len(
#                     app_tables.fin_loan_details.search(
#                         q.all_of(
#                             loan_updated_status=q.any_of(
#                                 q.like("disbursed loan%"),
#                                 q.like("foreclosure%"),
#                                 q.like("extension%")
#                             )
#                         ),
#                         lender_customer_id=user_profile['customer_id']
#                     )
#                 )

#                 lost_apportunity_loans = len(
#                     app_tables.fin_loan_details.search(
#                         q.all_of(
#                             loan_updated_status=q.any_of(
#                                 q.like("lost opportunities%"),                               
#                             )
#                         ),
#                         lender_customer_id=user_profile['customer_id']
#                     )
#                 )

#                 closed_loans = len(
#                     app_tables.fin_loan_details.search(
#                         q.all_of(
#                             loan_updated_status=q.any_of(
#                                 q.like("close%"),
                               
#                             )
#                         ),
#                         lender_customer_id=user_profile['customer_id']
#                     )
#                 )
              
#                 self.result.append({
#                     'customer_id': user_profile['customer_id'],
#                     'full_name': user_profile['full_name'],
#                     'email_user': user_profile['email_user'],
#                     'usertype': user_profile['usertype'],
#                     'last_confirm': user_profile['last_confirm'],
#                     'date_of_birth': user_profile['date_of_birth'],
#                     'mobile': user_profile['mobile'],
#                     'registration_approve': user_profile['registration_approve'],
#                     # 'credit_limit': credit_limit,                    
#                     'guarantor_name': guarantor_name,
#                     'guarantor_mobile_no': guarantor_ph_no,
#                     'another_person': guarantor,
#                     'lost_apportunity_loans':lost_apportunity_loans,
#                     'close': closed_loans,                    
#                     'membership': membership_type,
#                     'member_since': member_since,
#                     'user_photo':user_profile['user_photo'],
#                     'adhar': user_profile['aadhaar_no'],
#                 })
#             panel1_data = self.result[::2]  # Every second item starting from index 0
#             panel2_data = self.result[1::2]  # Every second item starting from index 1
            
#             # Bind data to the repeating panels
#             self.repeating_panel_1.items = panel1_data
#             self.repeating_panel_3.items = panel2_data 

#         if not self.result:
#             alert("No Lenders Available!")
#         else:
#             self.repeating_panel_1.items = self.result
#             # self.repeating_panel_2.items = self.result

#     def link_1_click(self, **event_args):
#         """This method is called when the link is clicked"""
#         open_form('admin.dashboard')

#     def search_lender(self, **event_args):
#       if not self.text_box_1.text.strip():
#         alert("The text box cannot be empty. Please enter some text.")
#         self.data_grid_1.visible = False
#       else:       
#         self.repeating_panel_2.items = anvil.server.call(
#         'search_lender',
#         self.text_box_1.text
#         )
#         self.data_grid_1.visible = True

#     def button_2_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('admin.dashboard.customer_management.handles_customer_registration')
      
from ._anvil_designer import lendersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lenders(lendersTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.data = app_tables.fin_user_profile.search()

        self.result = []
        for user_profile in self.data:
            if user_profile['usertype'] == 'lender':
                # Retrieve guarantor details from fin_guarantor table based on customer ID
                guarantor_record = app_tables.fin_guarantor_details.get(customer_id=user_profile['customer_id'])
                if guarantor_record is not None:
                    guarantor_name = guarantor_record['guarantor_name']
                    guarantor_ph_no = guarantor_record['guarantor_mobile_no']
                    guarantor = guarantor_record['another_person']
                else:
                    guarantor_name = None
                    guarantor_ph_no = None
                    guarantor = None

                loan_details = app_tables.fin_lender.get(customer_id=user_profile['customer_id'])
                if loan_details is not None:
                    membership_type = loan_details['membership']
                    member_since = loan_details['member_since']
                else:
                    membership_type = None
                    member_since = None

                # Count loan details with specific loan_updated_status
                loan_details_count = len(
                    app_tables.fin_loan_details.search(
                        q.all_of(
                            loan_updated_status=q.any_of(
                                q.like("disbursed loan%"),
                                q.like("foreclosure%"),
                                q.like("extension%")
                            )
                        ),
                        lender_customer_id=user_profile['customer_id']
                    )
                )

                lost_apportunity_loans = len(
                    app_tables.fin_loan_details.search(
                        q.all_of(
                            loan_updated_status=q.any_of(
                                q.like("lost opportunities%"),                               
                            )
                        ),
                        lender_customer_id=user_profile['customer_id']
                    )
                )

                closed_loans = len(
                    app_tables.fin_loan_details.search(
                        q.all_of(
                            loan_updated_status=q.any_of(
                                q.like("close%"),
                               
                            )
                        ),
                        lender_customer_id=user_profile['customer_id']
                    )
                )

                self.result.append({
                    'customer_id': user_profile['customer_id'],
                    'full_name': user_profile['full_name'],
                    'email_user': user_profile['email_user'],
                    'usertype': user_profile['usertype'],
                    'last_confirm': user_profile['last_confirm'],
                    'date_of_birth': user_profile['date_of_birth'],
                    'mobile': user_profile['mobile'],
                    'registration_approve': user_profile['registration_approve'],
                    'guarantor_name': guarantor_name,
                    'guarantor_mobile_no': guarantor_ph_no,
                    'another_person': guarantor,
                    'lost_apportunity_loans': lost_apportunity_loans,
                    'close': closed_loans,                    
                    'membership': membership_type,
                    'member_since': member_since,
                    'user_photo': user_profile['user_photo'],
                    'adhar': user_profile['aadhaar_no'],
                })

        panel1_data = self.result[::2]  # Every second item starting from index 0
        panel2_data = self.result[1::2]  # Every second item starting from index 1

        # Bind data to the repeating panels
        self.repeating_panel_1.items = panel1_data 
        self.repeating_panel_3.items = panel2_data 

        if not self.result:
            alert("No Lenders Available!")
        else:
            self.repeating_panel_1.items = self.result

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.dashboard')

    def search_lender(self, **event_args):
        if not self.text_box_1.text.strip():
            alert("The text box cannot be empty. Please enter some text.")
            self.data_grid_1.visible = False
        else:
            self.repeating_panel_2.items = anvil.server.call(
                'search_lender',
                self.text_box_1.text
            )
            self.data_grid_1.visible = True

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.customer_management.handles_customer_registration')
