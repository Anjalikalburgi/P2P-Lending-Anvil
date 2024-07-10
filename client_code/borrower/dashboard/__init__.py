from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from datetime import datetime, timezone, timedelta


SUPERSCRIPT_DIGITS = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

def to_superscript(number):
    return ''.join(SUPERSCRIPT_DIGITS.get(digit, '') for digit in str(number))

class dashboard(dashboardTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.email = main_form_module.email
        self.user_Id = main_form_module.userId
        self.notifications.text = "0"
        self.populate_loan_history()
        self.update_wallet_info()
        self.update_user_profile()
        self.load_notifications()
        self.update_platform_fees()
        self.image_1_copy_copy.role = 'circular-image'
         # Search for loans taken by the current user
        self.data= app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
        loan_count = len(self.data)

        # Update the UI with the count of loans
        self.label_9.text = str(loan_count)

        data = app_tables.fin_borrower.get(customer_id=self.user_Id)
        if data:
            self.label_5.text = data['credit_limit']
            self.label_7.text = data['borrower_since']

       

    def update_platform_fees(self, **event_args):
        result = anvil.server.call('update_fin_platform_fees')

    def populate_loan_history(self):
        try:
            customer_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
            if customer_loans:
                self.data = [{'product_name': loan['product_name'], 'loan_amount': loan['loan_amount'],
                              'tenure': loan['tenure'], 'interest_rate': loan['interest_rate'],
                              'total_repayment_amount': round(loan['total_repayment_amount'], 2),
                              'loan_updated_status': loan['loan_updated_status']} for loan in customer_loans]
                self.repeating_panel_1.items = self.data
            else:
                Notification("No Data Available Here!").show()
        except anvil.tables.TableError:
            alert("No data found")

    def update_wallet_info(self):
        wallet = app_tables.fin_wallet.get(customer_id=self.user_Id)
        if wallet:
            # self.label_9.text = "{:.2f}".format((wallet['wallet_amount'] or 0))
            self.label_2_copy_copy.text = "{:.2f}".format((wallet['wallet_amount'] or 0))

    def update_user_profile(self):
        user_profile = app_tables.fin_user_profile.get(customer_id=self.user_Id)
        if user_profile:
            self.label_3.text = user_profile['mobile']
            self.image_1_copy_copy.source = user_profile['user_photo']
            self.label_2_copy.text =  user_profile['full_name']

    def update_notification_count(self, count):
        self.notifications.text = str(count)

    def load_notifications(self):
        notifications = anvil.server.call('get_notifications', self.user_Id)
        unread_count = len([n for n in notifications if not n['read']])
        self.update_notification_count(unread_count)

    def notifications_click(self, **event_args):
        open_form('borrower.dashboard.borrower_notifications', user_Id=self.user_Id)

    def link_1_click(self, **event_args):
        try:
            existing_loans = app_tables.fin_loan_details.search(
                borrower_customer_id=self.user_Id,
                loan_updated_status=q.any_of(
                    q.like('accepted%'),
                    q.like('Approved%'),
                    q.like('approved%'),
                    q.like('under process%'),
                    q.like('foreclosure%'),
                    q.like('extension'),
                    q.like('disbursed%'),
                    q.like('Disbursed%'),
                    q.like('Under Process%'),
                    q.like('rejected')
                )
            )
            num_existing_loans = len(existing_loans)
            if num_existing_loans >= 5:
                alert("You already have 5 loans. Cannot open a new loan request.")
            else:
                wallet_row = app_tables.fin_wallet.get(customer_id=self.user_Id)
                if wallet_row and wallet_row['wallet_id'] is not None:
                    open_form('borrower.dashboard.new_loan_request')
                else:
                    alert("Wallet not found. Please create a wallet.")
        except anvil.tables.TableError as e:
            alert("Error fetching existing loans.")

    def link_2_click(self, **event_args):
        open_form('borrower.dashboard.today_dues')

    def link_3_click(self, **event_args):
        open_form('borrower.dashboard.view_loans')

    def link_4_click(self, **event_args):
        open_form('borrower.dashboard.foreclosure_request')

    def link_5_click(self, **event_args):
        open_form('borrower.dashboard.application_tracker')

    def link_6_click(self, **event_args):
        open_form('borrower.dashboard.extension_loan_request')

    def link_7_click(self, **event_args):
        open_form('borrower.dashboard.view_transaction_history')

    def link_8_click(self, **event_args):
        open_form('borrower.dashboard.discount_coupons')

    def link_10_click(self, **event_args):
        open_form('lendor.dashboard.lender_portfolio_first_page')

    def button_12_click(self, **event_args):
        open_form('borrower.dashboard.borrower_view_profile')

    def image_1_copy_copy_mouse_up(self, x, y, button, **event_args):
        open_form('borrower.dashboard.borrower_view_profile')

    def link_9_click(self, **event_args):
        customer_id = self.user_Id
        email = self.email
        anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
        open_form("wallet.wallet")

    def home_main_form_link_click(self, **event_args):
        open_form('borrower.dashboard')

    def about_main_form_link_click(self, **event_args):
        open_form("borrower.dashboard.dashboard_about")

    def contact_main_form_link_click(self, **event_args):
        open_form("borrower.dashboard.dashboard_contact")

    def link_11_click(self, **event_args):
        open_form('borrower.dashboard.dashboard_report_a_problem')

    def link_12_click(self, **event_args):
        pass

    def button_1_click(self, **event_args):
        customer_id = self.user_Id
        email = self.email
        anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
        open_form("wallet.wallet")
