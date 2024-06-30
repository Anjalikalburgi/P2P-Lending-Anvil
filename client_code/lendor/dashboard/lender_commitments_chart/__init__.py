from ._anvil_designer import lender_commitments_chartTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....bank_users.main_form import main_form_module
from ....bank_users.user_form import user_form
from ....bank_users.user_form import user_module
import datetime
import plotly.graph_objects as go
import anvil.media

class lender_commitments_chart(lender_commitments_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Fetch email and userId from main_form_module
    self.email = main_form_module.email
    print(self.email)
    self.user_id = main_form_module.userId
    
    # Create the charts
    self.create_pie_chart()

  def create_pie_chart(self):
    # Fetch data from the fin_lnder table
    lender_data = app_tables.fin_lender.search(customer_id=self.user_id)
    
    # Calculate total commitments and present commitments
    lender_total_commitments = sum((row['lender_total_commitments'] or 0) for row in lender_data)
    present_commitments = sum((row['present_commitments'] or 0) for row in lender_data)
    
    # Prepare data for the pie chart
    values = [lender_total_commitments, present_commitments]
    labels = ['Total Commitments', 'Present Commitments']
    
    # Create the pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    # Update the layout of the chart
    fig.update_layout(
      title_text="Lender Commitments",
      annotations=[
        dict(text='Total Commitments', x=0.82, y=0.5, font_size=12, showarrow=False),
        dict(text='Present Commitments', x=0.18, y=0.5, font_size=12, showarrow=False)
      ]
    )
    
    # Display the chart in the form
    self.plot_1.figure = fig

# You can remove or comment out this part if it was auto-generated and you don't use it
# The rest of your code should remain unchanged
