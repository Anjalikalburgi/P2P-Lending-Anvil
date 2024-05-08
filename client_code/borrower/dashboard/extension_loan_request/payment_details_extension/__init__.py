from ._anvil_designer import payment_details_extensionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import timedelta

class payment_details_extension(payment_details_extensionTemplate):
  def __init__(self, selected_row=None, loan_extension_months=None, extension_fee=None, **properties):
    self.selected_row = selected_row
    self.loan_extension_months = loan_extension_months
    self.extension_fee = extension_fee
    self.emi = None 
    self.init_components(**properties)

    if selected_row:
      self.load_payment_details(selected_row)

  def load_payment_details(self, selected_row):
    self.load_entered_values()
    payment_details = []

    entered_extension_months = self.loan_extension_months
    total_tenure = selected_row['tenure'] + entered_extension_months

    monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12

    beginning_balance = selected_row['loan_amount']

    extension_fee_percentage = self.extension_fee if self.extension_fee is not None else selected_row.get('extension_fee', 0)
    extension_fee_amount = (extension_fee_percentage / 100) * selected_row['loan_amount']

    # Find the last paid EMI number for the specific loan
    last_paid_emi_records = app_tables.fin_emi_table.search(loan_id=selected_row['loan_id'], scheduled_payment_made=q.not_(None))
    last_paid_emi_number = max([record['emi_number'] for record in last_paid_emi_records], default=0)
    print("last_paid_emi_number", last_paid_emi_number)
    last_paid_emi_ending_balance = selected_row['loan_amount']

    # Counter for payment number
    # payment_number_counter = last_paid_emi_number + 1
    payment_number_counter =   1

    # Adjust the total tenure to include extension months
    for month in range(1, total_tenure + 1):
      emi = 0  # Assign a default value
      payment_date = self.calculate_payment_date(selected_row, month)
      loan_id = selected_row['loan_id']
      emi_number = payment_number_counter
      emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=emi_number)

      if emi_row is not None:
        scheduled_payment_made = emi_row['scheduled_payment_made']
        account_number = emi_row['account_number']
      else:
        scheduled_payment_made = None
        account_number = None

      formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"

      if month <= last_paid_emi_number:
        # emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
        # total_payment = emi
        if selected_row['emi_payment_type'] == 'Monthly':
          emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
        elif selected_row['emi_payment_type'] == 'One Time':
          pass
        elif selected_row['emi_payment_type'] == 'Three Months':

          emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (selected_row['tenure']/3))
        elif selected_row['emi_payment_type'] == 'Six Months':

          emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (selected_row['tenure']/6))
        total_payment = emi
      else:
        if selected_row['emi_payment_type'] == 'Monthly':
          emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, total_tenure)
        elif selected_row['emi_payment_type'] == 'One Time':
                self.generate_one_time_payment_details(selected_row, extension_fee_amount)
                return
        elif selected_row['emi_payment_type'] == 'Three Months':
          if (month - last_paid_emi_number) % 3 == 0:
            emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (total_tenure/3))
        elif selected_row['emi_payment_type'] == 'Six Months':
          if (month - last_paid_emi_number) % 6 == 0:
            emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (total_tenure/6))

      # If the calculated emi is non-zero, calculate principal and other details
      if emi != 0:
        total_payment = emi + extension_fee_amount if payment_number_counter == (last_paid_emi_number + 1) else emi
        # last_paid_emi_ending_balance += extension_fee_amount
        interest_amount = last_paid_emi_ending_balance * monthly_interest_rate
        principal_amount = min(last_paid_emi_ending_balance, emi - interest_amount)  # Limit principal to remaining balance
        ending_balance = last_paid_emi_ending_balance - principal_amount
        payment_details.append({
            'PaymentNumber': payment_number_counter,
            'PaymentDate': formatted_payment_date,
            'EMIDate': f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A",
            'EMITime': f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A",
            'AccountNumber': account_number if account_number else "N/A",
            'ScheduledPayment': f"₹ {emi:.2f}",
            'Principal': f"₹ {principal_amount:.2f}",
            'Interest': f"₹ {interest_amount:.2f}",
            'BeginningBalance': f"₹ {last_paid_emi_ending_balance :.2f}" if last_paid_emi_ending_balance else "N/A",
            'ExtensionFee': f"₹ {extension_fee_amount:.2f}"  if payment_number_counter == (last_paid_emi_number + 1) else "₹ 0.00",
            'TotalPayment': f"₹ {total_payment:.2f}",
            'EndingBalance': f"₹ {ending_balance:.2f}"
        })

        last_paid_emi_ending_balance = ending_balance
        payment_number_counter += 1  # Increment payment number

    self.repeating_panel_1.items = payment_details


  def load_entered_values(self):
    self.entered_loan_amount = self.selected_row['loan_amount']
    self.entered_tenure = self.selected_row['tenure']
    self.entered_extension_months = self.loan_extension_months


  def calculate_payment_date(self, selected_row, current_month):
    loan_updated_status = selected_row['loan_updated_status'].lower()

    if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
        loan_id = selected_row['loan_id']

        # Search for the row in loan_details_table based on the loan_id
        loan_details_row = app_tables.fin_loan_details.get(loan_id=loan_id)
        if loan_details_row:
            loan_disbursed_timestamp = loan_details_row['loan_disbursed_timestamp']

            if loan_disbursed_timestamp:
                emi_payment_type = selected_row['emi_payment_type']

                if emi_payment_type == 'Monthly':
                    payment_date = loan_disbursed_timestamp + timedelta(days=30 * current_month)
                elif emi_payment_type == 'Three Months':
                    payment_date = loan_disbursed_timestamp + timedelta(days=90 * (current_month // 3))
                elif emi_payment_type == 'Six Months':
                    payment_date = loan_disbursed_timestamp + timedelta(days=180 * (current_month // 6))
                else:
                    payment_date = None

                return payment_date
            else:
                return None
        else:
            return None
    else:
        return None


  def calculate_scheduled_payment(self, loan_amount, monthly_interest_rate, remaining_tenure):
    emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_tenure)) / (
            ((1 + monthly_interest_rate) ** remaining_tenure) - 1)

    return emi

  

  def button_1_click(self, **event_args):
    # Find the index of the row where the extension fee is applied
    extension_fee_row_index = next(
        (i for i, item in enumerate(self.repeating_panel_1.items) if item.get('ExtensionFee', '') != '₹ 0.00'), None)

    if extension_fee_row_index is not None:
        # Extract the new EMI from the next row after the extension fee is applied
        if self.selected_row['emi_payment_type'] == 'One Time' and extension_fee_row_index + 1 >= len(self.repeating_panel_1.items):
            new_emi_amount = float(self.repeating_panel_1.items[extension_fee_row_index]['ScheduledPayment'].replace('₹ ', ''))
        else:
            new_emi_amount = float(self.repeating_panel_1.items[extension_fee_row_index + 1]['ScheduledPayment'].replace('₹ ', ''))

        # Find the month number for the extension
        extension_month_number = self.repeating_panel_1.items[extension_fee_row_index]['PaymentNumber']

        print(f"New EMI passed to extension2 form: {new_emi_amount}")
        print(f"Extension applied in month number: {extension_month_number}")

        # Pass the new EMI and extension month number to the extension2 form
        open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension.extension2',
                    selected_row=self.selected_row, loan_extension_months=self.loan_extension_months, new_emi=new_emi_amount, emi_number=extension_month_number)
    else:
        alert("Extension fee not found in payment details.")
  def button_2_click(self, **event_args):
    open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row=self.selected_row)
  def generate_one_time_payment_details(self, selected_row, extension_fee_amount):
    # Fetch required details from loan_details_table for one-time payment
    loan_details_row = app_tables.fin_loan_details.get(loan_id=selected_row['loan_id'])
    if loan_details_row:
        loan_updated_status = loan_details_row['loan_updated_status'].lower()
        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            loan_disbursed_timestamp = loan_details_row['loan_disbursed_timestamp']
            if loan_disbursed_timestamp:
                # Calculate the payment date for total tenure
                total_tenure_days = selected_row['tenure'] + self.loan_extension_months  # Total tenure in days
                payment_date = loan_disbursed_timestamp + timedelta(days=30 * total_tenure_days)
                formatted_payment_date = payment_date.strftime('%Y-%m-%d')
            else:
                formatted_payment_date = "N/A"

            beginning_balance = loan_details_row['total_repayment_amount'] + extension_fee_amount
            principal_amount = loan_details_row['loan_amount']
            interest_amount = loan_details_row['total_interest_amount']  # For one-time payment, interest is assumed to be zero
            total_payment = beginning_balance
            scheduled_payment = principal_amount + interest_amount
            ending_balance = 0

            # Append data to payment_details list
            payment_details = [{
                'PaymentNumber': 1,
                'PaymentDate': formatted_payment_date,
                'EMIDate': "N/A",
                'EMITime': "N/A",
                'AccountNumber': "N/A",
                'ScheduledPayment': f"₹ {scheduled_payment:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'ExtensionFee': f"₹ {extension_fee_amount:.2f}",
                'TotalPayment': f"₹ {total_payment:.2f}",
                'EndingBalance': "₹ 0.00"
            }]

            self.repeating_panel_1.items = payment_details
        else:
            print("Loan status not suitable for generating one-time payment details.")
    else:
        # Handle case where loan details are not found
        print("Loan details not found for loan ID:", selected_row['loan_id'])