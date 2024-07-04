# from ._anvil_designer import notifications_view_profileTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class notifications_view_profile(notifications_view_profileTemplate):
#     def __init__(self, customer_id, loan_id,data, **properties):
#         self.init_components(**properties)
#         self.customer_id = customer_id
#         self.loan_id = loan_id
#         self.data = data
#         self.load_borrower_details()

#     def load_borrower_details(self):
#         user_profile = app_tables.fin_user_profile.get(customer_id=self.customer_id)
#         loan = app_tables.fin_loan_details.get(loan_id=self.loan_id)
#         lender_details = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
#         if user_profile:
#             self.label_2.text = lender_details['full_name']
#             self.label_4.text = lender_details['mobile']
#             self.label_6.text = loan['product_name']
#             self.label_8.text = loan['loan_amount']
#             self.label_10.text = loan['tenure']
#             self.label_12.text = loan['interest_rate']
#             self.label_13.text = self.data
#             # Add other details as required

#     def button_2_click(self, **event_args):
#         open_form('borrower.dashboard.borrower_notifications',self.customer_id)


from ._anvil_designer import notifications_view_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class notifications_view_profile(notifications_view_profileTemplate):
    def __init__(self, customer_id, loan_id, data, **properties):
        self.init_components(**properties)
        self.customer_id = customer_id
        self.loan_id = loan_id
        self.data = data
        self.load_borrower_details()

    def load_borrower_details(self):
        user_profile = app_tables.fin_user_profile.get(customer_id=self.customer_id)
        loan = app_tables.fin_loan_details.get(loan_id=self.loan_id)
        lender_details = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
        if user_profile and loan and lender_details:
            self.label_2.text = lender_details['full_name']
            self.label_4.text = lender_details['mobile']
            self.label_6.text = loan['product_name']
            self.label_8.text = str(loan['loan_amount'])
            self.label_10.text = str(loan['tenure'])
            self.label_12.text = str(loan['interest_rate'])
            self.label_13.text = self.data

    def button_2_click(self, **event_args):
        open_form('borrower.dashboard.borrower_notifications', self.customer_id)
