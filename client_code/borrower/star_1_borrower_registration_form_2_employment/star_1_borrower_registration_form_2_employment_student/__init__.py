from ._anvil_designer import star_1_borrower_registration_form_2_employment_studentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class star_1_borrower_registration_form_2_employment_student(star_1_borrower_registration_form_2_employment_studentTemplate):
  def __init__(self,user_id, **properties):
    self.user_id=user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
     self.borrower_college_name_text.text=user_data['college_name']
     self.borrower_college_id_text.text=user_data['college_id']
     self.borrower_college_address_text.text=user_data['college_address']
     user_data.update()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  def button_1_copy_1_copy_1_copy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=self.user_id)

  def home_borrower_registration_form_copy_1_click(self, **event_args):
    open_form('bank_users.user_form')

  def button_1_next_copy_1_click(self, **event_args):
    college_name=self.borrower_college_name_text.text
    college_id=self.borrower_college_id_text.text
    college_proof=self.borrower_college_proof_img.file
    college_address=self.borrower_college_address_text.text
    user_id=self.user_id
    if not re.match(r'^[A-Za-z\s]+$', college_name):
      alert('enter valid college name')
      
    elif not college_name or not college_id or not college_proof or not college_address:
      Notification("please fill all requrired fields").show()
    else:
      anvil.server.call('add_borrower_student',college_name,college_id,college_proof,college_address,user_id)
      open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital',user_id=user_id)

  def borrower_college_proof_img_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.borrower_college_proof_img.file
