 
from ._anvil_designer import edit_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class edit_form(edit_formTemplate):
    def __init__(self,value_to_display, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        product = app_tables.fin_product_details.get(product_id=value_to_display)

        # Check if product exists
        if product is None:
            alert("No Data Available Here!!")
        else:
            # Populate form fields with product details
            self.label_1.text = str(product['product_id'])
            self.product_name.text = product['product_name']
            self.text_box_1.text = product['product_group']
            self.text_area_1.text = str(product['product_discription'])
            self.text_box_2.text = product['product_categories']
            self.text_box_3.text = str(product['processing_fee'])
            self.text_box_4.text = str(product['extension_fee'])
            self.foreclose_type.selected_value = product['foreclose_type']
            self.foreclosure_fee.text = str(product['foreclosure_fee'])
            self.extension_allowed.selected_value = str(product['extension_allowed'])
            self.drop_down_2.selected_value = product['membership_type']
            selected_interest_type = str(product['interest_type'])
            if selected_interest_type == "Fixed":
                    self.radio_button_1.selected = True
                    self.radio_button_2.enabled = False
                    self.button_1_1.enabled = False
                    self.button_2_1.enabled = False
                    self.button_3_1.enabled = False  
                    self.button_4_1.enabled = False 
                    self.text_area_1.enabled = False
                    self.product_name.enabled = False
                    self.min_amount.enabled = False
                    self.text_box_1.enabled = False
                    self.max_amount.enabled = False
                    self.min_tenure.enabled = False
                    self.max_tenure.enabled = False
                    self.roi.enabled = False
                    self.foreclosure_fee.enabled = False
                    self.foreclose_type.enabled = False
                    self.extension_allowed.enabled = False
                    self.min_months.enabled = False
                    self.text_box_2.enabled = False
                    self.text_box_3.enabled = False
                    self.text_box_4.enabled = False
                    self.business.enabled = False
                    self.student.enabled = False
                    self.employee.enabled = False
                    self.lapsed.enabled = False
                    self.default.enabled = False
                    self.npa.enabled = False
                    self.drop_down_2.enabled = False
               
            elif selected_interest_type == "Variable":
                    self.radio_button_1.enabled = False
                    self.radio_button_2.selected = True
                    self.button_1_1.enabled = False
                    self.button_2_1.enabled = False
                    self.button_3_1.enabled = False  
                    self.button_4_1.enabled = False 
                    self.text_area_1.enabled = False
                    self.product_name.enabled = False
                    self.min_amount.enabled = False
                    self.text_box_1.enabled = False
                    self.max_amount.enabled = False
                    self.min_tenure.enabled = False
                    self.max_tenure.enabled = False
                    self.roi.enabled = True
                    self.foreclosure_fee.enabled = False
                    self.foreclose_type.enabled = False
                    self.extension_allowed.enabled = False
                    self.min_months.enabled = False
                    self.text_box_2.enabled = False
                    self.text_box_3.enabled = False
                    self.text_box_4.enabled = False
                    self.business.enabled = False
                    self.student.enabled = False
                    self.employee.enabled = False
                    self.lapsed.enabled = False
                    self.default.enabled = False
                    self.npa.enabled = False
                    self.drop_down_2.enabled = False
               
            else:
                print(f"Unexpected interest type: {selected_interest_type}")

            self.roi.text = str(product['roi'])
            self.min_amount.text = str(product['min_amount'])
            self.max_amount.text = str(product['max_amount'])
            self.min_tenure.text = str(product['min_tenure'])
            self.max_tenure.text = str(product['max_tenure'])
            self.min_months.text = str(product['min_months'])
            self.lapsed.text = str(product['lapsed_fee'])
            self.default.text = str(product['default_fee'])
            self.npa.text = str(product['npa'])

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      selected_product_id = self.label_1.text  # Assuming the product ID is displayed in a label
  
      if selected_product_id == "":
          alert("Please select a product to update.")
      else:
          data = app_tables.fin_product_details.get(product_id=selected_product_id)
          if data is None:
              alert("No Data Available Here")            
          else:
              # Update only if interest type is Variable
              #if self.radio_button_2.selected:  # Checking if interest type is Variable
                  data['roi'] = int(self.roi.text)  # Update the interest rate
                  Notification("Details updated successfully").show()
                  open_form('admin.dashboard.manage_products')
              # else:
                  #alert("Cannot edit details for Fixed interest type.")

    def button_1_copy_3_click(self, **event_args):
        open_form('admin.dashboard.manage_products.view_product')

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("admin.dashboard")

    


