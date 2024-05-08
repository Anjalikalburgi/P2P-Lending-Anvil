from ._anvil_designer import star_1_borrower_registration_form_2_employment_emp_detail_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_2_employment_emp_detail_2(star_1_borrower_registration_form_2_employment_emp_detail_2Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['company_address']
      self.text_box_2.text=user_data['company_landmark']
      self.text_box_3.text=user_data['business_no']
      user_data.update()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    comp_address = self.text_box_1.text
    landmark = self.text_box_2.text
    business_phone_number = self.text_box_3.text
    user_id = self.userId

    if not business_phone_number.isdigit():
        Notification("Business number should be valid").show()
    elif not comp_address or not landmark or not business_phone_number:
      Notification("please fill the required fields").show()
    
    else:
      anvil.server.call('add_lendor_individual_form_2',comp_address,landmark,business_phone_number,user_id)
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=user_id)


  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_1',user_id=self.userId)

  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
