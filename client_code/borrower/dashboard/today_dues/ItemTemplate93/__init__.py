from ._anvil_designer import ItemTemplate93Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate93(ItemTemplate93Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_1.role = 'circular-image'

    # Any code you write here will run before the form opens.

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    selected_row = self.item
    product_id = selected_row['product_id']

    product_details = app_tables.fin_product_details.get(product_id=product_id)
    if product_details:
        product_name = product_details['product_name']
        description = product_details['product_description']
        category = product_details['product_categories']
        membership = product_details['membership_type']
        interest_type = product_details['interest_type']
        product_id = product_details['product_id']
        emi_payment_type = product_details['emi_payment']

      
        
        # Display the product details in a notification
        alert(
            f"Product Name: {product_name}\n"
            f"Product Id: {product_id}\n"
            f"Description: {description}\n"
            f"Category: {category}\n"
            f"Membership Type: {membership}"
            f"Interest Type: {interest_type}\n"
            f"Emi payment Type: {emi_payment_type}\n"
        )
    else:
        Notification("Product details not found.").show()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    open_form('borrower.dashboard.today_dues.check_out', selected_row = selected_row)

  def view_details_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    open_form('borrower.dashboard.today_dues.payment_details_t', selected_row = selected_row)

    
