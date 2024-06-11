from ._anvil_designer import stack_graphTemplate
from anvil import *
import plotly.graph_objs as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class stack_graph(stack_graphTemplate):
  def __init__(self, selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.selected_row = selected_row
    self.loan_id = self.selected_row['loan_id']
    
    # Fetch the relevant data
    self.loan_details = app_tables.fin_loan_details.search(loan_id=self.loan_id)
    self.emi_details = app_tables.fin_emi_table.search(loan_id=self.loan_id)
    
    # Prepare data for the plot
    self.prepare_and_show_graph()
    
  def prepare_and_show_graph(self):
    # Prepare the data for the stack graph
    loan_ids = []
    emi_numbers = []
    days_left_data = []
    
    for loan_detail in self.loan_details:
      loan_id = loan_detail['loan_id']
      for emi_detail in self.emi_details:
        if emi_detail['loan_id'] == loan_id:
          loan_ids.append(loan_id)
          emi_numbers.append(emi_detail['emi_number'])
          days_left_data.append(emi_detail['days_left'])
    
    # Create traces for each unique loan_id
    traces = []
    unique_loan_ids = list(set(loan_ids))
    for loan_id in unique_loan_ids:
      emi_nums = [emi_numbers[i] for i in range(len(loan_ids)) if loan_ids[i] == loan_id]
      days_left = [days_left_data[i] for i in range(len(loan_ids)) if loan_ids[i] == loan_id]
      
      trace = go.Scatter(
        x=emi_nums, 
        y=days_left, 
        mode='lines+markers',
        name=f'Loan ID: {loan_id}',
        marker=dict(color='#dc143c'),
        line=dict(color='#dc143c')
      )
      traces.append(trace)
    
    # Create the figure with the traces
    fig = {
      'data': traces,
      'layout': go.Layout(
        title='EMI Tracking',
        xaxis={'title': 'EMI Number'},
        yaxis={'title': 'Days passed due date'},
        showlegend=True
      )
    }
    
    # Show the graph in the form
    self.plot_1.data = fig['data']
    self.plot_1.layout = fig['layout']

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules.port_folio_risk')
