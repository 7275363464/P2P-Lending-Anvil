from ._anvil_designer import view_productTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# class view_product(view_productTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     # Any code you write here will run before the form opens.
#     self.data = tables.app_tables.product_details.search()

#     a = -1
#     self.list_1 = []
#     self.list_2 = []
#     self.list_3 = []
#     self.list_4 = []
#     self.list_5 = []

#     for i in self.data:
#       a+=1
#       self.list_1.append(i['product_id'])
#       self.list_2.append(i['product_group'])
#       self.list_3.append(i['product_categories'])
#       self.list_4.append(i['processing_fee'])
#       self.list_5.append(i['extension_fee'])


#     self.result = []
#     if a == -1:
#       alert("No Data Available Here!")
#     else:
#       for i in range(a+1):
#         self.result.append({'product_id' : self.list_1[i], 'product_group' : self.list_2[i], 'product_categories' : self.list_3[i], 'processing_fee' : self.list_4[i], 'extension_fee' : self.list_5[i]})

#       self.repeating_panel_1.items = self.result


#   def link_1_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.dashboard.manage_products')

#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('admin.dashboard.manage_products.edit_form')

#   def button_2_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('admin.dashboard.manage_products.update_form')

class view_product(view_productTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.fetch_and_populate_data()

    def fetch_and_populate_data(self):
        self.data = tables.app_tables.fin_product_details.search()

        if not self.data:
            Notification("No Data Available Here!").show()
        else:
            self.result = [{'product_id': i['product_id'],
                            'product_group': i['product_group'],
                            'product_categories': i['product_categories'],
                            'processing_fee': i['processing_fee'],
                            'extension_fee': i['extension_fee']}
                           for i in self.data]

            self.repeating_panel_1.items = self.result

    def link_1_click(self, **event_args):
        open_form('admin.dashboard.manage_products')

    def button_1_click(self, **event_args):
        open_form('admin.dashboard.manage_products.edit_form')

    def button_2_click(self, **event_args):
        open_form('admin.dashboard.manage_products.update_form')
