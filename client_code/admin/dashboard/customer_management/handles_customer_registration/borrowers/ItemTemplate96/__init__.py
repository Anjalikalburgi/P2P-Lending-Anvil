from ._anvil_designer import ItemTemplate96Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate96(ItemTemplate96Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.user_id = main_form_module.userId   
    # user_data = app_tables.fin_loan_details.search()
    # for row in user_data:
    #     borrower_customer_id = row['borrower_customer_id']
    #     lender_customer_id = row['lender_customer_id']
    #     borrower_profile = app_tables.fin_user_profile.get(customer_id=borrower_customer_id)
    #     lender_profile = app_tables.fin_user_profile.get(customer_id=lender_customer_id)
    #     self.image_1.source = borrower_profile['user_photo']


    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    value_to_pass = self.link_1.text
    open_form('admin.dashboard.customer_management.handles_customer_registration.borrowers.view_profile', value_to_pass)