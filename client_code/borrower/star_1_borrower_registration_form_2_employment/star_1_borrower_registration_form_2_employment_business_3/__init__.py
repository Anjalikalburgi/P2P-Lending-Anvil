from ._anvil_designer import star_1_borrower_registration_form_2_employment_business_3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_2_employment_business_3(star_1_borrower_registration_form_2_employment_business_3Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_3.text=user_data['din']
      self.text_box_4.text=user_data['cin']
      self.text_box_1.text=user_data['registered_off_add']
      # if user_data['proof_verification']:
      #    self.file_loader_1.url = anvil.media.get_url(user_data['proof_verification'])
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def button_2_click(self, **event_args):
    din = self.text_box_3.text
    cin = self.text_box_4.text
    reg_off_add = self.text_box_1.text
    proof_verification = self.file_loader_1.file
    user_id = self.userId
    if not din or not cin or not reg_off_add or not proof_verification:
      Notification("Please all the fields").show()
    else:
     anvil.server.call('add_lendor_institutional_form_3',din,cin,reg_off_add,proof_verification,user_id)
     open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital',user_id=user_id)

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_2',user_id=user_id)
    

  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.file_loader_1.file
