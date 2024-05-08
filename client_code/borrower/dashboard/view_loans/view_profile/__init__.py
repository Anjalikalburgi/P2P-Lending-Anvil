from ._anvil_designer import view_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...import main_form_module as main_form_module
from datetime import datetime, date

class view_profile(view_profileTemplate):
    def __init__(self, selected_row, **properties):
        self.selected_row = selected_row
        self.init_components(**properties)

        # Display loan details
        self.loan_id_label.text = f"{selected_row['loan_id']}"
        self.loan_amount_label.text = f"{selected_row['loan_amount']}"
        self.intrest_rate_label.text = f"{selected_row['interest_rate']}"
        self.tenure_label.text = f"{selected_row['tenure']}"
        
        timestamp = selected_row['borrower_loan_created_timestamp']
        if isinstance(timestamp, date):
            date_of_apply = timestamp  # No need to convert if it's already a date
        else:
            date_of_apply = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").date()

        self.date_of_apply_label.text = f"{date_of_apply}"

        loan_updated_status = selected_row['loan_updated_status']
        self.loan_updated_status_label.text = f"{loan_updated_status}"

        # Check if the loan status is 'rejected' and set the foreground color to red
        if loan_updated_status.lower() == 'rejected':
            self.loan_updated_status_label.foreground = 'red'

    def button_1_copy_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')

    def button_1_click(self, **event_args):
        open_form('borrower_registration_form.dashboard.view_loans')

    def link_1_click(self, **event_args):
      open_form('borrower_registration_form.dashboard.view_loans.payment_details_b', selected_row=self.selected_row, entered_values=None)