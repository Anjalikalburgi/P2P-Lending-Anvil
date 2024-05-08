from ._anvil_designer import view_profileTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module
#from .. import borrower_main_form_module as main_form_module

class view_profile(view_profileTemplate):
    def __init__(self, selected_row, **properties):
        self.init_components(**properties)

        # Display loan details
        self.loan_id_label.text = f"{selected_row['loan_id']}"
        self.loan_amount_label.text=f"{selected_row['loan_amount']}"
        self.intrest_rate_label.text=f"{selected_row['interest_rate']}"
        self.tenure_label.text=f"{selected_row['tenure']}"
        self.date_of_apply_label.text=f"{selected_row['borrower_loan_created_timestamp']}"
        self.loan_updated_status_label.text=f"{selected_row['loan_updated_status']}"
    def button_1_copy_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.application_tracker')
