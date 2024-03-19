from ._anvil_designer import add_subcategoryTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_subcategory(add_subcategoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()

    # Any code you write here will run before the form opens.

  def refresh(self):
    """Refresh repeating panels with the latest data"""
    self.repeating_panel_1.items = app_tables.fin_admin_beseem_categories.search(group_name="gender")
    self.repeating_panel_2.items = app_tables.fin_admin_beseem_categories.search(group_name="qualification")
    self.repeating_panel_3.items = app_tables.fin_admin_beseem_categories.search(group_name="marital_status")
    self.repeating_panel_5.items = app_tables.fin_admin_beseem_categories.search(group_name="profession")
    self.repeating_panel_4.items = app_tables.fin_admin_beseem_categories.search(group_name="all_loans")
    self.repeating_panel_6.items = app_tables.fin_admin_beseem_categories.search(group_name="organization_type")
    self.repeating_panel_7.items = app_tables.fin_admin_beseem_categories.search(group_name="present_address")
    self.repeating_panel_8.items = app_tables.fin_admin_beseem_categories.search(group_name="duration_at_address")
    self.repeating_panel_9.items = app_tables.fin_admin_beseem_categories.search(group_name="salary_type")
    self.repeating_panel_10.items = app_tables.fin_admin_beseem_categories.search(group_name='spouse_profession')
    self.repeating_panel_11.items = app_tables.fin_admin_beseem_categories.search(group_name='age_of_business')
  
  def back_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("admin.dashboard.manage_bessem")
    
  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_1.text.lower()
    entered_min_pts = int(self.text_box_2.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='gender',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_1.text = ' '
    self.text_box_2.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='gender')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="gender")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="gender", max_points=max_points
        )

  def qualification_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_3.text.lower()
    entered_min_pts = int(self.text_box_4.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='qualification',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_3.text = ' '
    self.text_box_4.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='qualification')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="qualification")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="qualification", max_points=max_points
        )

  def marrital_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_5.text.lower()
    entered_age = self.text_box_5a.text.lower()
    entered_min_pts = int(self.text_box_6.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='marital_status',sub_category=entered_sub,min_points=entered_min_pts,age=entered_age)
    self.text_box_5.text = ' '
    self.text_box_5a.text = ' '
    self.text_box_6.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='marital_status')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="marital_status")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="marital_status", max_points=max_points
        )

  def profession_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_7.text.lower()
    # valid_statuses = ['student', 'employee', 'self employment']
    # if entered_sub not in valid_statuses:
    #     alert("Please enter a valid profession: 'Student', 'Employee', 'Self employment'.")
    #     return
    entered_min_pts = int(self.text_box_8.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='profession',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_7.text = ' '
    self.text_box_8.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='profession')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="profession")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="profession", max_points=max_points
        )
    
  def all_loans_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_9.text.lower()
    entered_yes_no = self.text_box_10.text.lower()
    valid_statuses = ['yes', 'no']
    if entered_yes_no not in valid_statuses:
        alert("Kindly input either 'Yes' or 'No'.")
        return
    entered_min_pts = int(self.text_box_11.text)
    
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='all_loans',sub_category=entered_sub,min_points=entered_min_pts,is_liveloan=entered_yes_no)
    self.text_box_9.text = ' '
    self.text_box_10.text = ' '
    self.text_box_11.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='all_loans')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="all_loans")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="all_loans", max_points=max_points
        )

  def organization_type_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_12.text.lower()
    entered_min_pts = int(self.text_box_13.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='organization_type',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_12.text = ' '
    self.text_box_13.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='organization_type')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="organization_type")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="organization_type", max_points=max_points
        )

  def present_address_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_14.text.lower()
    entered_min_pts = int(self.text_box_15.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='present_address',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_14.text = ' '
    self.text_box_15.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='present_address')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="present_address")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="present_address", max_points=max_points
        )

  def duration_at_address_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_16.text.lower()
    entered_min_pts = int(self.text_box_17.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='duration_at_address',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_16.text = ' '
    self.text_box_17.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='duration_at_address')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="duration_at_address")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="duration_at_address", max_points=max_points
        )

  def salarytype_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_18.text.lower()
    entered_min_pts = int(self.text_box_19.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='salary_type',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_18.text = ' '
    self.text_box_19.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='salary_type')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="salary_type")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="salary_type", max_points=max_points
        )

  def spouse_profession_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    entered_sub = self.text_box_20.text.lower()
    entered_min_pts = int(self.text_box_21.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='spouse_profession',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_20.text = ' '
    self.text_box_21.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='spouse_profession')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="spouse_profession")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="spouse_profession", max_points=max_points
        )

  def age_of_business_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_22.text.lower()
    entered_min_pts = int(self.text_box_23.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='age_of_business',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_22.text = ' '
    self.text_box_23.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='age_of_business')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="age_of_business")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="age_of_business", max_points=max_points
        )
    
  def salary_type_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = True
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False
    
  def gender_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = True
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def qualification_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = True
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def marrital_status_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = True
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def profession_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = True
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def home_loan_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = True
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def organization_type_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = True
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def present_address_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = True
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def duration_at_address_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = True
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = False

  def spouse_profession_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = True
    self.grid_panel_11.visible = False

  def age_of_business_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False
    self.grid_panel_6.visible = False
    self.grid_panel_7.visible = False
    self.grid_panel_8.visible = False
    self.grid_panel_9.visible = False
    self.grid_panel_10.visible = False
    self.grid_panel_11.visible = True

  

  

  
  
  