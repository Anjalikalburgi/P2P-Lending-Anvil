from ._anvil_designer import extension2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class extension2(extension2Template):
    def __init__(self, selected_row, loan_extension_months, new_emi, emi_number, **properties):
        self.init_components(**properties)
        self.selected_row = selected_row
        self.extension_months = loan_extension_months
        self.new_emi = new_emi
        self.emi_number = emi_number 
        self.label_23.text = f"{selected_row['loan_id']}"
        self.mi_label.text = f"{selected_row['loan_amount']}"

        loan_id = selected_row['loan_id']

        # Fetching the total_repayment_amount from the loan_details table
        fin_loan_details_row = app_tables.fin_loan_details.get(loan_id=loan_id)

        if fin_loan_details_row:
            total_loan_amount = fin_loan_details_row['total_repayment_amount']
            print(f"Total Repayment Amount: {total_loan_amount}")
        else:
            total_loan_amount = 0  # Set a default value if the row is not found
            print("Total Repayment Amount not found in fin_loan_details table.")

        # Continue with the rest of the initialization code
        loan_id_str = str(selected_row['loan_id'])
        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id_str)

        if last_emi_rows:
            last_emi_list = list(last_emi_rows)
            if last_emi_list:  # Check if the list is not empty
                last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)
                total_payments_made = last_emi_list[0]['emi_number']
            else:
                total_payments_made = 0
                print("No rows found for the given loan_id in 'fin_emi_table'")
        else:
            total_payments_made = 0
            print("No rows found for the given loan_id in 'fin_emi_table'")

        print("total payment made", total_payments_made)
        loan_amount = int(self.mi_label.text)

        # Additional initialization code
        tenure = selected_row['tenure']
        tenure = int(tenure)
        self.interest_rate = selected_row['interest_rate']
        monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)
        factor = (1 + monthly_interest_rate) ** tenure
        emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
        emi = int(emi)
        monthly_installment = loan_amount / tenure
        monthly_installment = int(monthly_installment)
        print(f"loan_amount: {loan_amount}")
        print(f"emi: {emi}")
        print(f"monthly installment: {monthly_installment}")

        product_id_to_search = selected_row['product_id']
        data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
        self.extension_fee_lst = []
        for i in data:
            self.extension_fee_lst.append(i['extension_fee'])

        self.extension_fee.text = self.extension_fee_lst[0]
        extension_fee = int(self.extension_fee.text)
        loan_amount = int(self.mi_label.text)
        extension_amount = (extension_fee * loan_amount) / 100
        print('extension_amount', extension_amount)
        self.extension_amountt.text = extension_amount
        emi_paid = total_payments_made * emi
        print('emi_paid', emi_paid)
        remaining_loan_amount = (total_loan_amount - emi_paid) + extension_amount
        print('remaining_loan_amount', remaining_loan_amount)
        outstanding_months = tenure - total_payments_made
        print(outstanding_months)

        # Calculate the new EMI amount for the extended period
        total_extension_months =  self.extension_months  # Including the current month

        # if total_payments_made > 0:
        #     remaining_tenure = outstanding_months + self.extension_months
        #     new_emi_amount = remaining_loan_amount / remaining_tenure
        #     new_emi_amount += extension_amount
        # else:
        new_emi_amount = self.new_emi  # Use the provided new_emi value

        # Save the calculated values as instance variables for later use
        self.total_extension_months = total_extension_months
        self.extension_fee_comp_value = extension_fee
        self.remaining_loan_amount = remaining_loan_amount
        self.final_repayment.text = f"₹ {remaining_loan_amount:.2f}"
        self.new_emii.text = f"₹ {new_emi_amount:.2f}"

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.f_checkbox.checked:
            # Get the reason entered by the user
            reason = self.reason_textbox.text.strip()
            loan_id = self.selected_row['loan_id']
            loan_details_rows = app_tables.fin_loan_details.search(loan_id=loan_id)
    
            if loan_details_rows:
                loan_details_row = loan_details_rows[0]  # Assuming there's only one matching row
                borrower_customer_id = loan_details_row['borrower_customer_id']
                borrower_email_id = loan_details_row['borrower_email_id']
                borrower_full_name = loan_details_row['borrower_full_name']
            else:
                borrower_customer_id = None
                borrower_email_id = None
                borrower_full_name = None
            final_repayment_numeric = float(self.final_repayment.text.replace('₹', '').replace(',', '').strip())
            new_emi_numeric = float(self.new_emii.text.replace('₹', '').replace(',', '').strip())
            if borrower_customer_id is not None and borrower_email_id is not None and borrower_full_name is not None and reason:
                app_tables.fin_extends_loan.add_row(
                    loan_id=self.selected_row['loan_id'],
                    borrower_full_name= borrower_full_name,
                    loan_amount=self.selected_row['loan_amount'],
                    borrower_customer_id= borrower_customer_id,
                    borrower_email_id= borrower_email_id,
                    extend_fee=self.extension_fee_comp_value,
                    final_repayment_amount= final_repayment_numeric,
                    extension_amount=self.extension_amountt.text,
                    new_emi= new_emi_numeric,
                    total_extension_months=self.total_extension_months,
                    reason=reason,
                    status='under process',
                    emi_number=self.emi_number,
                    extension_request_date=datetime.now()
                )
                alert("Extension request submitted successfully!", title="Success")
                open_form('borrower_registration_form.dashboard.extension_loan_request')
            elif not reason:
                alert('Please enter a reason for extension.')
            else:
              alert('The selected row does not contain the borrower_customer_id. Please check your data.')
        else:
            alert('Please accept the Terms and Conditions.')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row=self.selected_row)
