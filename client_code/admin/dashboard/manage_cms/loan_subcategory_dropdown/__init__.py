from ._anvil_designer import loan_subcategory_dropdownTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class loan_subcategory_dropdown(loan_subcategory_dropdownTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.add_report_issues_dropdown')

  def borrower_loan_issue(self, **event_args):
    self.column_panel_10.visible = True
    self.column_panel_11_copy.visible = False
    self.column_panel_12_copy_2.visible = False
    self.repeating_panel_1.items = app_tables.fin_borrower_subcategory_loan_issue.search()


  def lender_loan_issue(self, **event_args):
    self.column_panel_10.visible = False
    self.column_panel_11_copy.visible = False
    self.column_panel_12_copy_2.visible = True
    self.repeating_panel_3.items = app_tables.fin_lender_subcategory_loan_issue.search()


  def technical_issue(self, **event_args):
    self.column_panel_10.visible = False
    self.column_panel_11_copy.visible = True
    self.column_panel_12_copy_2.visible = False
    self.repeating_panel_2.items = app_tables.fin_subcategory_technical_issue.search()

  def borrower_issue(self, **event_args):
    enter_data = self.text_box_9.text

    if not enter_data:
        alert("Please enter a valid Borrower Loan Issues: 'Loan Not Approved', 'Loan declained', 'Other'.")
        return
    app_tables.fin_borrower_subcategory_loan_issue.add_row(borrower_subcategory_loan_issue=enter_data)
    self.text_box_9.text = ' '
    self.repeating_panel_1.items = app_tables.fin_borrower_subcategory_loan_issue.search()

  def technical_issue_click(self, **event_args):
    enter_data = self.text_box_9_copy.text
  
    if not enter_data:
          alert("Please enter a valid Technical Issues: 'Button Not Working', 'Page Not Working', 'Other'.")
          return
    app_tables.fin_subcategory_technical_issue.add_row(subcategory_technical_issue=enter_data)
    self.text_box_9_copy.text = ' '
    self.repeating_panel_2.items = app_tables.fin_subcategory_technical_issue.search()

  def lender_issue_click(self, **event_args):
    enter_data = self.text_box_9_copy_2.text
  
    if not enter_data:
          alert("Please enter a valid Technical Issues: 'Loan Not Approved', 'Amount Not Credited', 'Other'.")
          return
    app_tables.fin_lender_subcategory_loan_issue.add_row(lender_subcategory_loan_issue=enter_data)
    self.text_box_9_copy_2.text = ' '
    self.repeating_panel_3.items = app_tables.fin_lender_subcategory_loan_issue.search()

