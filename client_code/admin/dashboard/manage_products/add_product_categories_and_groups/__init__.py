from ._anvil_designer import add_product_categories_and_groupsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_product_categories_and_groups(add_product_categories_and_groupsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    options = app_tables.fin_product_group.search()
    option_strings = [option['name'] for option in options]
    self.drop_down_1.items = option_strings
    self.drop_down_1.selected_value = option_strings[0] if option_strings else None

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_products')

  def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Get selected values
      selected_group = self.drop_down_1.selected_value
      text_box_value = self.text_box_1.text
  
      # Check if both values are selected or entered
      if selected_group and text_box_value:
          # Split the entered categories based on comma
          categories_list = [category.strip() for category in text_box_value.split(',')]
  
          # Create a new row in the product_categories table for each category
          for category in categories_list:
              app_tables.fin_product_categories.add_row(
                  name_group=selected_group,
                  name_categories=category
              )
  
          # Optionally, you can show a confirmation message
          alert("Product categories saved successfully!")
  
          # Clear the input fields after saving
          self.drop_down_1.selected_value = None
          self.text_box_1.text = ""
          # open_form('admin.dashboard.manage_products')
      else:
          # Show an error message if one or both values are not selected or entered
          alert("Please enter/select all details before saving.")

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_products.add_group')


  
  
