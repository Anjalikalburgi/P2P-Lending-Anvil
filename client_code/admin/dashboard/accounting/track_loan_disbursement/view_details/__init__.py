from ._anvil_designer import view_detailsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class view_details(view_detailsTemplate):
  def __init__(self, selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Store the selected row
    self.selected_row = selected_row
    print(self.selected_row)
    print(selected_row['loan_id'])
   
    self.borrower_full_name.text = f"{selected_row['borrower_full_name']}"
    self.borrower_email.text = f"{selected_row['borrower_email_id']}"
    self.name.text = f"{selected_row['lender_full_name']}"
    self.lender_email.text = f"{selected_row['lender_email_id']}"
    self.interest.text = f"{selected_row['interest_rate']}"
    self.loan_amount.text = f"{selected_row['loan_amount']}"
    self.status.text = f"{selected_row['loan_updated_status']}"
    self.repay_amount.text = "{0.2f}.{selected_row['total_repayment_amount']}"
    self.membership.text = f"{selected_row['membership_type']}"
    self.emi.text = f"{selected_row['emi_payment_type']}"
    self.product_name.text = f"{selected_row['product_name']}"
