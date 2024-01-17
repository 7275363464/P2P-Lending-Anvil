from ._anvil_designer import EditDetailsFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert

class EditDetailsForm(EditDetailsFormTemplate):
    def __init__(self, selected_row, **properties):
        self.init_components(**properties)

        # Set the initial values for the input components
        self.text_box_1.text = selected_row['name']
        
        # Store the selected row for later use
        self.selected_row = selected_row

    def button_1_click(self, **event_args):
        """Save changes button click event"""
        # Get the updated value from the input component
        updated_group = self.text_box_1.text.lower()  # Convert to lowercase

        # Check if the updated value is the same as the existing value
        if updated_group != self.selected_row['name'].lower():
            # Convert the existing group names to lowercase for case-insensitive comparison
            existing_names_lower = [row['name'].lower() for row in app_tables.fin_product_group.search()]
            
            if updated_group in existing_names_lower:
                alert(f'Group "{self.text_box_1.text}" already exists. Please choose a different name.')
            else:
                # Update the existing row in the product_categories table
                self.selected_row['name'] = updated_group

                # Save changes to the database
                self.selected_row.update()

                alert("Changes saved successfully!")
                open_form('admin.dashboard.manage_products.view_products_and_categories')

        else:
            # No changes were made
            alert("No changes made.")
            open_form('admin.dashboard.manage_products.view_products_and_categories')
          
    def button_2_click(self, **event_args):
        """Cancel button click event"""
        # Close the form without saving changes
        open_form('admin.dashboard.manage_products.view_products_and_categories')

    def delete_button(self, **event_args):
        """Delete button click event"""
        # Confirm the deletion with the user
        confirmation = alert(
            "Are you sure you want to delete this group?",
            title="Confirm Deletion",
            buttons=[("Cancel", False), ("Delete", True)],
        )

        if confirmation:
            # Get the name of the group to be deleted
            group_name = self.selected_row['name'].lower()

            # Delete the rows from the product_group table
            self.selected_row.delete()

            # Delete the corresponding rows from the product_categories table
            categories_to_delete = app_tables.fin_product_categories.search(q.any_of(name_group=group_name))
            for category_row in categories_to_delete:
                category_row.delete()

            alert("Group and corresponding categories deleted successfully!")
            open_form('admin.dashboard.manage_products.view_products_and_categories')

    def home_button(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard')
