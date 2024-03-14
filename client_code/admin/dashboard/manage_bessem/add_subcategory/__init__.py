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
    self.repeating_panel_3.items = app_tables.fin_admin_beseem_categories.search(group_name="marrital_status")
    self.repeating_panel_5.items = app_tables.fin_admin_beseem_categories.search(group_name="profession")
    self.repeating_panel_4.items = app_tables.fin_admin_beseem_categories.search(group_name="all_loans")

  def back_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("admin.dashboard.manage_bessem")
    
  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_1.text
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
    entered_sub = self.text_box_3.text
    valid_statuses = ['10th Class', 'Intermediate / PUC', "Bachelor's", "Master's", 'PhD']
    if entered_sub not in valid_statuses:
        alert("Please enter a valid qualification: '10th Class', 'Intermediate / PUC', 'Bachelor's', 'Master's', 'PhD'.")
        return
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
    entered_sub = self.text_box_5.text
    entered_age = self.text_box_5a.text
    entered_min_pts = int(self.text_box_6.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='marrital_status',sub_category=entered_sub,min_points=entered_min_pts,age=entered_age)
    self.text_box_5.text = ' '
    self.text_box_5a.text = ' '
    self.text_box_6.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='marrital_status')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="marrital_status")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="marrital_status", max_points=max_points
        )

  def profession_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_7.text
    valid_statuses = ['Student', 'Employee', 'Business']
    if entered_sub not in valid_statuses:
        alert("Please enter a valid profession: 'Student', 'Employee', 'Business'.")
        return
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
    entered_sub = self.text_box_9.text
    entered_yes_no = self.text_box_10.text
    valid_statuses = ['Yes', 'No']
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
    
  def gender_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = True
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False

  def qualification_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = True
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False

  def marrital_status_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = True
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = False

  def profession_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = True
    self.grid_panel_5.visible = False

  def all_loans_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False
    self.grid_panel_4.visible = False
    self.grid_panel_5.visible = True
  
