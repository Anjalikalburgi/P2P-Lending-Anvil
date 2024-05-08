from ._anvil_designer import star_1_borrower_registration_form_2_employment_business_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class star_1_borrower_registration_form_2_employment_business_2(star_1_borrower_registration_form_2_employment_business_2Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.date_picker_1.date = user_data['year_estd']
      self.text_box_1.text=user_data['industry_type']
      self.text_box_2.text=user_data['six_month_turnover']
      # if user_data['last_six_month_bank_proof']:
      #   self.file_loader_1.file = user_data['last_six_month_bank_proof']
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def button_2_click(self, **event_args):
    year = self.date_picker_1.date
    industry_type = self.text_box_1.text
    turn_over = self.text_box_2.text
    last_six_statements = self.file_loader_1.file
    user_id = self.userId
    if not year or not industry_type or not turn_over or not last_six_statements:
      Notification("Please fill all the fields").show()
    else:
     today = datetime.today()
     months = today.year * 12 + today.month - year.year * 12 - year.month
     anvil.server.call('add_lendor_institutional_form_2',year,months,industry_type,turn_over,last_six_statements,user_id)
     open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_3',user_id = user_id)

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id = user_id)
    """This method is called when the button is clicked"""

  def home_borrower_registration_form_copy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.user_form')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.file_loader_1.file
