from ._anvil_designer import star_1_borrower_registration_form_education_intermediateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_education_intermediate(star_1_borrower_registration_form_education_intermediateTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)




    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    user_id = self.userId
    open_form('borrower_registration_form.star_1_borrower_registration_form_1_education',user_id=user_id)
    

  def button_2_click(self, **event_args):
     """This method is called when the button is clicked"""
     user_id = self.userId
     tenth_class = self.file_loader_1.file
     intermediate = self.file_loader_2.file
    
     if not tenth_class or not intermediate:
       Notification('Please upload both files before proceed.').show()
     else:
       anvil.server.call('add_education_int',tenth_class,intermediate,user_id)
       open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=user_id)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_1.source = self.file_loader_1.file

  def file_loader_2_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file:
      self.image_2.source = self.file_loader_2.file

