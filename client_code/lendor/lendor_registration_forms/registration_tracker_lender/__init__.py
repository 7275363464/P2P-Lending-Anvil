from ._anvil_designer import registration_tracker_lenderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....bank_users.main_form import main_form_module
from ....bank_users.main_form import main_form
from ....bank_users.user_form import user_module


class registration_tracker_lender(registration_tracker_lenderTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.email = main_form_module.email
        email = self.email
        self.user_id = user_module.find_user_id(email)
        
        user_id = self.user_id
        
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        
        # List of labels to be highlighted based on form count
        labels = [
            (self.label_1,),
            (self.label_13, self.label_2),
            (self.label_14, self.label_3),
            (self.label_15, self.label_4),
            (self.label_16, self.label_6)
        ]
        
        # Set initial opacity for all labels
        for label_pair in labels:
            for label in label_pair:
                label.foreground = "rgba(0, 0, 0, 0.5)"  # Set to semi-transparent

        # Initialize form_count to 0 if user_data is None or form_count is None
        form_count = user_data['form_count'] if user_data and user_data['form_count'] is not None else 0
        
        print(form_count)
        
        for i in range(form_count + 1):
            if i < len(labels):
                for label in labels[i]:
                    label.bold = True
                    label.foreground = "rgba(0, 0, 0, 1)"  # Set to fully opaque
                
                # Set the icon for the first label in each pair
                if i == 0:
                    self.label_7.icon = '_/theme/bank_users/circle-1_1.png'                    
                elif i == 1:
                    self.label_8.icon = '_/theme/bank_users/circle-2%20(2).png'
                elif i == 2:
                    self.label_9.icon = '_/theme/bank_users/circle-3%20(2).png'
                elif i == 3:
                    self.label_10.icon = '_/theme/bank_users/circle-4%20(2).png'
                else:
                    self.label_11.icon = '_/theme/bank_users/circle-5%20(2).png'
