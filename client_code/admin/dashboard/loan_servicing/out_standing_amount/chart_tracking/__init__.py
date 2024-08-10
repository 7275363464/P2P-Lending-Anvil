from ._anvil_designer import chart_trackingTemplate
from anvil import *
import plotly.graph_objs as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class chart_tracking(chart_trackingTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Store selected row data
        self.selected_row = selected_row
        self.loan_id = self.selected_row['loan_id']
        self.total_repayment_amount = self.selected_row['total_repayment_amount']
        extension_months = self.get_extension_details(self.loan_id)
        self.tenure = self.selected_row['tenure'] + extension_months

        if self.selected_row['remaining_tenure'] =='N/A':
            self.remaining_amount = 0
            self.remaining_tenure = 0
        else:
            self.remaining_tenure = self.selected_row['tenure'] - self.selected_row['remaining_tenure']
            self.remaining_amount = self.selected_row['total_repayment_amount'] - self.selected_row['remaining_amount']

        # If remaining tenure is 0, set remaining amount to 0
        # if self.selected_row['remaining_tenure'] == 0:
        #     self.remaining_amount = 0
        #     self.remaining_tenure = 0

        # Call the function to create the plot
        self.create_plot()
        
    def create_plot(self):
        # Data for the plot
        total_repayment = go.Scatter(
            name='Total Repayment',
            x=[0, self.tenure],  # X-axis: From 0 to total tenure
            y=[0, self.total_repayment_amount],  # Y-axis: From 0 to total repayment amount
            mode='lines+markers'
        )
        
        remaining_repayment = go.Scatter(
            name='Remaining Repayment',
            x=[0, self.remaining_tenure],  # X-axis: From 0 to remaining tenure
            y=[0, self.remaining_amount],  # Y-axis: From 0 to remaining amount
            mode='lines+markers'
        )

        # Create the figure
        fig = go.Figure(data=[total_repayment, remaining_repayment])

        # Update the layout
        fig.update_layout(
            title='Repayment Amount Over Tenure',
            xaxis_title='Tenure',
            yaxis=dict(
                title='Amount',
                range=[0, self.total_repayment_amount * 1.1]  # Set y-axis range to slightly above the total repayment amount
            ),
            showlegend=True
        )

        # Embed the plot in the form
        # Ensure you have a Plotly component named plot_1 in your Anvil form
        self.plot_1.figure = fig

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.loan_servicing.out_standing_amount')

    def get_extension_details(self, loan_id):
        extension_row = app_tables.fin_extends_loan.get(
            loan_id=loan_id,
        )
        extension_months = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_months = extension_row['total_extension_months']
        return  extension_months