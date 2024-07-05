from ._anvil_designer import editTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class edit(editTemplate):
  def __init__(self,loan_details,emi_details,extension_details,foreclosure_details, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.loan_details = loan_details
    self.emi_details = emi_details
    self.extension_details = extension_details
    print(extension_details)
    self.foreclosure_details = foreclosure_details

    if loan_details:
      self.loan_details_column_panel_1.visible = True

      self.processing_fee.text = loan_details['total_processing_fee_amount']
      self.loan_id_label.text = loan_details['loan_id']
      self.borrower_id.text = loan_details['borrower_customer_id']
      self.borrower_email.text = loan_details['borrower_email_id']
      self.borrower_name.text = loan_details['borrower_full_name']
      self.product_id.text = loan_details['product_id']
      self.updated_status.text = loan_details['loan_updated_status']
      self.interest_amount.text = loan_details['total_interest_amount']
      self.total_repayment_amount.text = loan_details['total_repayment_amount']
      self.remaining_amount.text = loan_details['remaining_amount']
      self.loan_amount.text = loan_details['loan_amount']
      self.product_name.text = loan_details['product_name']
      self.membership_type.text = loan_details['membership_type']
      self.interest_rate.text = loan_details['interest_rate']
      self.tenure.text = loan_details['tenure']
      self.leneder_id.text = loan_details['lender_customer_id']
      self.lender_returnss.text = loan_details['lender_returns']
      self.lender_email.text = loan_details['lender_email_id']
      self.disbursed_date_picker_2.date = loan_details['loan_disbursed_timestamp']
      self.emi_payment_type.text = loan_details['emi_payment_type']
      self.first_date_picker_1.date = loan_details['first_emi_payment_due_date']
      self.total_amount.text = loan_details['total_amount_paid']


    
    elif emi_details:
      self.emi_panel.visible = True

      self.borrower_id_copy.text = emi_details['borrower_customer_id']
      self.loan_id_label_copy.text = emi_details['loan_id']
      # self.borrower_id.text = emi_details['borrower_customer_id']
      self.borrower_email_copy.text = emi_details['borrower_email']
      # self.borrower_name.text = emi_details['borrower_full_name']
      self.schedule_payment_made.text = emi_details['scheduled_payment_made']
      self.account_no.text = emi_details['account_number']
      self.remaining_tenure.text = emi_details['remaining_tenure']
      self.days_left.text = emi_details['days_left']
      self.emi_number.text = emi_details['emi_number']
      self.schedule_date_picker_1_copy.date = emi_details['scheduled_payment']
      self.next_date_picker_2_copy.date = emi_details['next_payment']
      self.leneder_id_copy.text = emi_details['lender_customer_id']
      self.lender_email_copy.text = emi_details['lender_email']
      self.Total_amount_paid.text = emi_details['amount_paid']
      self.total_repayment_amount_copy.text = emi_details['total_remaining_amount']
      self.lender_returns.text = emi_details['lender_returns']
      self.platform_fee.text = emi_details['total_platform_fee']
      self.extra_fee.text = emi_details['extra_fee']
      self.payment_payment_date.text = emi_details['part_payment_date']
      self.part_payment_amount.text = emi_details['part_payment_amount']
      self.Payment_type.text = emi_details['payment_type']
      
    elif extension_details:
      self.extension_panel.visible = True

      self.E_status.text = extension_details['status']
      self.E_reason.text = extension_details['reason']
      self.E_emi.text = extension_details['new_emi']
      self.E_loan_amount_copy_2.text = extension_details['loan_amount']
      self.E_extension_amount.text = extension_details['extension_amount']
      self.E_borrower_id_copy_2.text = extension_details['borrower_email_id']
      self.E_lender_email_copy_2.text = extension_details['lender_email_id']
      self.Extesnion_request_datepicker.date = extension_details['extension_request_date']
      self.E_borrower_name_copy_2.text = extension_details['borrower_full_name']
      self.E_leneder_id_copy_2.text = extension_details['lender_customer_id']
      self.E_borrower_id_copy_2.text = extension_details['borrower_customer_id']
      self.E_extension_months.text = extension_details['total_extension_months']
      self.E_emi_number.text = extension_details['emi_number']
      self.E_approved_date.text = extension_details['status_timestamp ']


    
    elif foreclosure_details:
      self.forelosure_panel.visible = True

      self.foreclosure_fee.text = foreclosure_details['foreclose_fee']
      self.F_interest_rate_copy_3.text = foreclosure_details['interest_rate']
      self.F_borrower_name_copy_3.text = foreclosure_details['borrower_name']
      self._Floan_id_label_copy_3.text = foreclosure_details['loan_id']
      self.F_reason.text = foreclosure_details['reason']
      self.foreclosure_amount.text = foreclosure_details['foreclose_amount']
      self.F_loan_amount.text = foreclosure_details['loan_amount']
      self.F_requested_on.date = foreclosure_details['requested_on']
      self.total_due_amount.text = foreclosure_details['total_due_amount']
      self.F_status.text = foreclosure_details['status']
      self.F_emi_number.text = foreclosure_details['foreclosure_emi_num']
      self.F_leneder_id_copy_3.text = foreclosure_details['lender_customer_id']
      self.F_lender_email_copy_3.text = foreclosure_details['lender_email_id']
      self.F_product_name_copy_3.text = foreclosure_details['product_name']
      self.F_borrower_id_copy_3.text = foreclosure_details['borrower_customer_id']
      self.F_borrower_email_copy_3.text = foreclosure_details['borrower_email_id']
      self.F_status_timestamp.text = foreclosure_details['status_timestamp ']

  
    # Any code you write here will run before the form opens.

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.loan_management.editing_detabase_details')

  def loan_details_click(self, **event_args):
    """This method is called when the button is clicked"""
    loan = app_tables.fin_loan_details.get(loan_id=self.loan_details['loan_id'])
    if loan:
      loan['first_emi_payment_due_date'] = self.first_date_picker_1.date
      loan['loan_disbursed_timestamp'] = self.disbursed_date_picker_2.date
      loan.update()
      alert('details saved successfully')
      open_form('admin.dashboard.loan_management.editing_detabase_details')

  def emi_detaisl_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.emi_details['scheduled_payment'] = self.schedule_date_picker_1_copy.date
    self.emi_details['next_payment'] = self.next_date_picker_2_copy.date
    alert('details saved successfully')
    open_form('admin.dashboard.loan_management.editing_detabase_details')

  def emi_details_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.extension_details['extension_request_date'] = self.Extesnion_request_datepicker.date
    self.extension_details['emi_number'] = int(self.E_emi_number.text)
    self.extension_details['status'] = self.E_status.text
    alert('details saved successfully')
    open_form('admin.dashboard.loan_management.editing_detabase_details')

  def foreclosure_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.foreclosure_details['requested_on'] = self.F_requested_on.date
    self.foreclosure_details['foreclosure_emi_num'] = int(self.F_emi_number.text)
    self.foreclosure_details['status'] = self.F_status.text
    alert('details saved successfully')
    open_form('admin.dashboard.loan_management.editing_detabase_details')

