from ._anvil_designer import lender_registration_form_4_bank_form_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_4_bank_form_2(lender_registration_form_4_bank_form_2Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['bank_id']
      self.text_box_2.text=user_data['account_bank_branch']
    # user_data = anvil.server.call('get_user_data', user_id)
    # if user_data:
    #         self.bank_id = user_data.get('bank_id', '')
    #         self.branch_name = user_data.get('account_bank_branch', '')
            
    # else:
    #     self.bank_id = ''
    #     self.branch_name = ''

    #    #Restore previously entered data if available
    # if self.bank_id:
    #         self.text_box_1.text= self.bank_id
    # if self.branch_name:
    #       self.text_box_2.text = self.branch_name

  def button_2_click(self, **event_args):
    user_id = self.userId
    bank_id = self.text_box_1.text
    branch_name = self.text_box_2.text
    t_and_c = self.check_box_1_copy_3 
    
    if not bank_id  or not branch_name or not t_and_c:
      Notification("please fill all required fields").show()
    else:
      anvil.server.call('add_lendor_bank_details_form_2', bank_id,branch_name, user_id)
      open_form('lendor_registration_form.dashboard')

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id=self.userId)

  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
    
  def link_1_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('Agreements, Privacy Policy and Applicant should accept following:Please note that any information concealed (as what we ask for), would be construed as illegitimate action on your part and an intentional attempt to hide material information which if found in future, would attract necessary action (s) at your sole cost. Hence, request to be truthful to your best knowledge while sharing your details)')

  def check_box_1_copy_3_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.accepted_terms = self.check_box_1_copy_3.checked
    self.button_2.enabled = self.accepted_terms
