from ._anvil_designer import view_profile_7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_profile_7(view_profile_7Template):
    def __init__(self, loan_id_to_display, **properties):
        self.init_components(**properties)
        self.loan_data = app_tables.fin_loan_details.get(loan_id=loan_id_to_display)
        if self.loan_data:
            user_profile_data = app_tables.fin_user_profile.get(customer_id=self.loan_data['borrower_customer_id'])
            if user_profile_data:
                self.label_34_copy.text = user_profile_data['usertype']

            # Fetch additional data from fin_borrower table based on borrower_customer_id
            borrower_data = app_tables.fin_borrower.get(customer_id=self.loan_data['borrower_customer_id'])
            if borrower_data:
                self.label_26_copy.text = borrower_data['ascend_score']
          
            self.label_2_copy.text = self.loan_data['loan_id']
            self.label_4_copy.text = self.loan_data['borrower_customer_id']
            self.label_6_copy.text = self.loan_data['borrower_full_name']
            # self.label_8.text = self.loan_data['loan_status']
            # self.label_10.text = self.loan_data['application_status']
            self.label_16_copy.text = self.loan_data['interest_rate']
            self.label_18_copy.text = self.loan_data['borrower_loan_created_timestamp']
            self.label_20_copy.text = self.loan_data['total_repayment_amount']
            # self.label_22.text = self.loan_data['total_payments_made']
            self.label_28_copy.text = self.loan_data['borrower_email_id']
            self.label_30_copy.text = self.loan_data['tenure']
            self.label_32_copy.text = self.loan_data['loan_updated_status']

    def button_1_click(self, **event_args):
        open_form('admin.dashboard.loan_management.view_loans.default_loans')

    def button_2_click(self, **event_args):
        if self.loan_data:
            self.loan_data['loan_updated_status'] = 'OTS'
            self.loan_data.update()
            ots = app_tables.fin_user_profile.get(customer_id=self.loan_data['borrower_customer_id'])
            if ots:
                ots['one_time_settlement'] = True
            alert('Request Submited')
            self.button_2.visible = False
          
