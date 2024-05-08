from ._anvil_designer import new_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class new_loan_request(new_loan_requestTemplate):
    def __init__(self, **properties):
        self.user_id = main_form_module.userId
        self.product_description = None
        self.init_components(**properties)

        options = app_tables.fin_product_details.search()
        # Exclude empty strings from the drop-down options
        option_strings = [option['product_group'] for option in options if option['product_group'].strip()]
        unique_groups = set(option_strings)  # Remove duplicates using set
        self.name.items = list(unique_groups)
        self.name.selected_value = None  # Set to None initially, as there is no default selection

        # Add a placeholder to drop_down_2
        self.drop_down_2.items = ['']  # Add your placeholder text here
        self.drop_down_2.selected_value = None
        self.drop_down_1.items = ['']
        self.drop_down_1.selected_value = None

    def name_change(self, **event_args):
        self.selected_value = self.name.selected_value

        if self.selected_value:
            self.label_1.visible = True
            self.label_2.visible = True
            self.name.visible = True
            self.drop_down_2.visible = True
            self.label_4.visible = True
            # Fetch product categories based on the selected loan type
            product_categories = app_tables.fin_product_details.search(
                product_group=self.name.selected_value
            )
            # Exclude duplicate categories
            unique_categories = set(category['product_categories'] for category in product_categories if category['product_categories'].strip())
            if unique_categories:
                # Display unique product categories in drop_down_2
                self.drop_down_2.items = list(unique_categories)
                self.drop_down_2.selected_value = None

    def drop_down_2_change(self, **event_args):
        self.selected_value = self.drop_down_2.selected_value
        if self.selected_value:
            self.label_1.visible = True
            self.label_2.visible = True
            self.name.visible = True
            self.drop_down_2.visible = True
            self.label_4.visible = True
            self.label_6.visible = True
            self.label_7.visible = True
            self.drop_down_1.visible = True

            # Fetch product names based on the selected category
            product_names = app_tables.fin_product_details.search(product_categories=self.selected_value)
            if product_names:
                # Extract product names from the list of rows
                product_name_list = [product['product_name'] for product in product_names if product['product_name'].strip()]
                self.drop_down_1.items = product_name_list
                self.drop_down_1.selected_value = None

    def button_2_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')

    def button_1_copy_click(self, **event_args):
        name = self.name.selected_value
        category = self.drop_down_2.selected_value
        product_name = self.drop_down_1.selected_value

        if not name:
            self.label_3.text = "Please select a product group"
            self.label_3.foreground = '#FF0000'
        else:
            self.label_3.text = ""

        if not category:
            self.label_4.text = "Please select a category"
            self.label_4.foreground = '#FF0000'
        else:
            self.label_4.text = ""

        if not product_name:
            self.label_7.text = "Please select a product name"
            self.label_7.foreground = '#FF0000'
        else:
            self.label_7.text = ""

        if name and category and product_name:
            # Fetch product details based on the selected product name
            product_details = app_tables.fin_product_details.get(product_name=product_name)

            if product_details:
                # Set product_description as a class attribute
                self.product_description = product_details['product_description']

                # Open the next form and pass the required parameters
                open_form('borrower_registration_form.dashboard.new_loan_request.loan_type',
                          name, category, product_name, self.max_amount_lb.text, self.product_description)
            else:
                # Handle the case where product details are not found
                self.label_8.visible = True
                self.product_description_label.text = "Product description not available"
        else:
            # Handle the case where no product is selected
            self.label_8.visible = False
            self.product_description_label.text = ""

    def max_amount_lb_show(self, **event_args):
        data = app_tables.fin_borrower.search()
        # Exclude empty strings from the max_amount values
        data1_strings = [str(data['credit_limit']) for data in data if str(data['credit_limit']).strip()]
        self.max_amount_lb.text = data1_strings[0] if data1_strings else None

    def button_1_click(self, **event_args):
        open_form("borrower_registration_form.dashboard")

    def drop_down_1_change(self, **event_args):
        selected_product_name = self.drop_down_1.selected_value
    
        if selected_product_name:
            # Fetch product details based on the selected product name
            
            product_details = app_tables.fin_product_details.get(product_name=selected_product_name)
            
            if product_details:
                # Display product description in a label or another component
                self.label_8.visible = True
                self.product_description_label.text = product_details['product_description']
            else:
                # Handle the case where product details are not found
                self.label_8.visible = True
                self.product_description_label.text = "Product description not available"
        else:
            # Handle the case where no product is selected
            self.label_8.visible = False
            self.product_description_label.text = ""
