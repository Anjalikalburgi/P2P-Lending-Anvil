from ._anvil_designer import lender_registration_Institutional_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re

class lender_registration_Institutional_form_1(lender_registration_Institutional_form_1Template):
  def __init__(self, user_id,**properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['business_name']
      self.text_box_2.text=user_data['business_add']
      self.drop_down_1.selected_value=user_data['business_type']
      self.drop_down_2.selected_value = user_data['employees_working']
      
      user_data.update()
    # user_data = anvil.server.call('get_user_data', user_id)
        
    # if user_data:
    #         self.business_type = user_data.get('business_type', '')
    #         self.empolyees_working = user_data.get('employees_working', '')
    #         # self.year = user_data.get('year_estd', '')
    #         self.business_name = user_data.get('business_name', '')
    #         self.business_add = user_data.get('business_add', '')
  
            
    # else:
    #     self.business_type = ''
    #     self.empolyees_working = ''
    #     # self.year = ''
    #     self.business_name = ''
    #     self.business_add = ''
        

    #    #Restore previously entered data if available
    # if self.business_type:
    #         self.drop_down_1.items = self.business_type
    # if self.empolyees_working:
    #        self.drop_down_2.items = self.empolyees_working
    # # if self.year:
    # #        self.date_picker_1.date = self.year

    # if self.business_name:
    #         self.text_box_1.text= self.business_name
    # if self.business_add:
    #         self.text_box_2.text= self.business_add

    options = app_tables.fin_lendor_business_type.search()
    options_string = [str(option['lendor_business_type']) for option in options]
    self.drop_down_1.items = options_string

    options = app_tables.fin_lendor_no_of_employees.search()
    options_string = [str(option['lendor_no_of_employees']) for option in options]
    self.drop_down_2.items = options_string


  def button_2_click(self, **event_args):
    business_name = self.text_box_1.text
    business_add = self.text_box_2.text
    business_type = self.drop_down_1.selected_value
    empolyees_working = self.drop_down_2.selected_value
       
    user_id = self.userId
    
    if not re.match(r'^[A-Za-z\s]+$', business_name):
      alert('enter valid college name')
    elif not business_name or not business_add or not business_type or not empolyees_working:
      Notification("Please fill all the fields").show()
    else:
       anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
       open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_2',user_id = user_id)
   

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_2',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")
    
