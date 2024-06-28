from ._anvil_designer import due_dateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class due_date(due_dateTemplate):
    def __init__(self, **properties):
    # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.due_date_data()

    def due_date_data(self):
        # Fetch data from the fin_emi_table where default_fee is greater than or equal to 3
        emi_details = app_tables.fin_emi_table.search(days_left=q.greater_than_or_equal_to(3))
        
        result = []
        for emi in emi_details:
            borrower_id = emi['borrower_customer_id']
            user_profile = app_tables.fin_user_profile.get(customer_id=borrower_id)
            mobile_no = user_profile['mobile'] if user_profile else None

            result.append({
                'loan_id': emi['loan_id'],
                'borrower_customer_id': borrower_id,
                'borrower_full_name': user_profile['full_name'],
                'borrower_email_id': user_profile['email_user'],
                'mobile_no': mobile_no,
                'days_left': emi['days_left']
            })
        
        # Debug: Print the final result before setting it to the repeating panel
        print("Final result:", result)
        
        # Set the filtered data to the repeating panel
        self.repeating_panel_1.items = result


    # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
      open_form('admin.dashboard.accounting.mis_reports.behavioural_report')
