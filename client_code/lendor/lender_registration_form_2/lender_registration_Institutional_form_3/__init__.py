from ._anvil_designer import lender_registration_Institutional_form_3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_Institutional_form_3(lender_registration_Institutional_form_3Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = anvil.server.call('get_user_data', user_id)
        
    if user_data:
            self.reg_off_add = user_data.get('registered_off_add', '')
            self.din = user_data.get('din', '')
            self.cin= user_data.get('cin', '')
            
    else:
        self.reg_off_add = ''
        # self.off_add_proof = ''
        self.din = ''
        self.cin = ''
       
       #Restore previously entered data if available
    if self.reg_off_add:
            self.text_box_1.text= self.reg_off_add
    if self.din:
            self.text_box_3.text= self.din
    if self.cin:
            self.text_box_4.text= self.cin
    
    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    reg_office_add = self.text_box_1.text
    din = self.text_box_3.text
    cin = self.text_box_4.text
    proof_verification = self.file_loader_1.file
    user_id = self.userId
    if not reg_office_add  or not proof_verification or not din or not cin:
      Notification("Please all the fields").show()
    else:
     anvil.server.call('add_lendor_institutional_form_3',din, cin,reg_office_add,proof_verification, user_id)
     open_form('lendor_registration_form.lender_registration_form_3_marital_details',user_id=user_id)
    """This method is called when the button is clicked"""

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_2',user_id=user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.file_loader_1.file
    
